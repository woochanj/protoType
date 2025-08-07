#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
심리전 가위바위보 게임 매니저
"""

import pygame
import random
from typing import Tuple, Optional
from enum import Enum
from .player import Player, Choice
from .ai_player import AIPlayer
from .font_utils import get_korean_font

class GameState(Enum):
    MODE_SELECTION = "모드 선택"
    SETUP = "데미지 배분"
    PLAYING = "게임 진행"
    ROUND_RESULT = "라운드 결과"
    DEATH_ANIMATION = "사망 애니메이션"
    GAME_OVER = "게임 종료"

class GameMode(Enum):
    PRACTICE = "연습모드"
    STORY = "스토리모드"

class GameManager:
    def __init__(self):
        """게임 매니저 초기화"""
        self.state = GameState.MODE_SELECTION
        self.game_mode = None
        self.player = Player("플레이어", 50, 100)
        self.computer = AIPlayer("컴퓨터", 550, 100)
        
        # 라운드 정보
        self.round_number = 1
        self.round_result = None
        self.round_damage = 0
        
        # 애니메이션 관련 속성
        self.animation_frame = 0
        self.animation_duration = 120  # 2초 (60fps 기준)
        self.dead_player = None  # 사망한 플레이어
        self.health_bar_fragments = []  # 체력바 파편들
        
        # UI 요소 - 한글 폰트 사용
        self.font = get_korean_font(36)
        self.small_font = get_korean_font(24)
        
        # 색상
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        # 컴퓨터 AI 설정
        self.setup_computer_damage()
    
    def set_game_mode(self, mode: GameMode):
        """게임 모드 설정"""
        self.game_mode = mode
        self.state = GameState.SETUP
        print(f"게임 모드 선택: {mode.value}")
    
    def get_game_mode(self) -> Optional[GameMode]:
        """게임 모드 반환"""
        return self.game_mode
    
    def go_home(self):
        """홈 화면으로 돌아가기"""
        self.state = GameState.MODE_SELECTION
        self.game_mode = None
        print("홈 화면으로 돌아갑니다.")
    
    def setup_computer_damage(self):
        """컴퓨터 데미지 배분 설정"""
        # 랜덤하게 데미지 배분 (총합 20)
        total = 20
        scissors = random.randint(0, total)
        remaining = total - scissors
        rock = random.randint(0, remaining)
        paper = remaining - rock
        
        self.computer.set_damage_allocation(scissors, rock, paper)
    
    def get_winner(self, choice1: Choice, choice2: Choice) -> Optional[Player]:
        """승자 결정"""
        if choice1 == choice2:
            return None  # 무승부
        
        # 상성 규칙
        if (choice1 == Choice.SCISSORS and choice2 == Choice.PAPER) or \
           (choice1 == Choice.ROCK and choice2 == Choice.SCISSORS) or \
           (choice1 == Choice.PAPER and choice2 == Choice.ROCK):
            return self.player
        else:
            return self.computer
    
    def calculate_damage(self, winner: Player, choice: Choice) -> int:
        """데미지 계산"""
        base_damage = winner.damage_allocation[choice]
        
        # 특수 능력 적용
        special_multiplier = winner.get_special_ability_damage_multiplier()
        
        # 연속 보너스 적용
        bonus_multiplier = winner.get_bonus_damage_multiplier()
        
        # 최종 데미지 계산
        final_damage = int(base_damage * special_multiplier * bonus_multiplier)
        
        return final_damage
    
    def process_round(self):
        """라운드 처리"""
        player_choice = self.player.get_choice()
        computer_choice = self.computer.get_choice()
        
        if player_choice is None or computer_choice is None:
            return
        
        # AI가 플레이어 선택 기록
        self.computer.record_player_choice(player_choice)
        self.computer.record_ai_choice(computer_choice)
        
        winner = self.get_winner(player_choice, computer_choice)
        
        if winner:
            damage = self.calculate_damage(winner, winner.get_choice())
            loser = self.computer if winner == self.player else self.player
            
            # 바위 특수 능력 적용 (승리한 플레이어가 바위를 선택했을 때)
            if winner.get_choice() == Choice.ROCK and winner.special_ability_active:
                winner.apply_rock_special_ability()
            
            # 연속 보너스 적용
            winner.record_win()
            loser.record_loss()
            
            # 보너스 데미지 사용 후 리셋
            if winner.bonus_damage > 0:
                winner.reset_bonus_damage()
            
            loser.take_damage(damage)
            self.round_damage = damage
        else:
            self.round_damage = 0
        
        # AI가 라운드 결과 기록
        self.computer.record_round_result(player_choice, computer_choice, winner)
        
        self.round_result = {
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'winner': winner,
            'damage': self.round_damage
        }
        
        # 체력이 0 이하가 되었는지 확인
        if not self.player.is_alive() or not self.computer.is_alive():
            dead_player = self.computer if not self.computer.is_alive() else self.player
            self.start_death_animation(dead_player)
        else:
            self.state = GameState.ROUND_RESULT
    
    def next_round(self):
        """다음 라운드로 진행"""
        self.round_number += 1
        self.player.reset_choice()
        self.computer.reset_choice()
        self.round_result = None
        self.state = GameState.PLAYING
    
    def check_game_over(self) -> bool:
        """게임 종료 확인"""
        if not self.player.is_alive() or not self.computer.is_alive():
            if self.state != GameState.DEATH_ANIMATION:  # 이미 애니메이션 중이면 무시
                self.state = GameState.GAME_OVER
            return True
        return False
    
    def get_winner_player(self) -> Optional[Player]:
        """게임 승자 반환"""
        if not self.player.is_alive():
            return self.computer
        elif not self.computer.is_alive():
            return self.player
        return None
    
    def computer_choose(self):
        """컴퓨터 선택"""
        # AI 패턴 분석 기반 선택
        choice = self.computer.make_choice()
        self.computer.set_choice(choice)
    
    def get_state(self) -> GameState:
        """현재 게임 상태 반환"""
        return self.state
    
    def set_state(self, state: GameState):
        """게임 상태 설정"""
        self.state = state
    
    def get_round_info(self) -> dict:
        """라운드 정보 반환"""
        return {
            'round_number': self.round_number,
            'result': self.round_result,
            'player_health': self.player.health,
            'computer_health': self.computer.health
        }
    
    def reset_game(self):
        """게임 리셋"""
        self.player.health = self.player.max_health
        self.computer.health = self.computer.max_health
        self.player.reset_choice()
        self.computer.reset_choice()
        self.round_number = 1
        self.round_result = None
        self.state = GameState.MODE_SELECTION
        self.game_mode = None
        self.setup_computer_damage()

    def start_death_animation(self, dead_player: Player):
        """사망 애니메이션 시작"""
        self.dead_player = dead_player
        self.animation_frame = 0
        self.state = GameState.DEATH_ANIMATION
        self.create_health_bar_fragments()
        print(f"{dead_player.name} 사망! 애니메이션 시작...")
    
    def create_health_bar_fragments(self):
        """체력바 파편 생성"""
        self.health_bar_fragments = []
        # 체력바 위치에 파편들 생성
        if self.dead_player == self.player:
            base_x, base_y = 50, 100
        else:
            base_x, base_y = 550, 100
        
        # 여러 개의 파편 생성
        for i in range(8):
            fragment = {
                'x': base_x + i * 10,
                'y': base_y,
                'vx': random.randint(-5, 5),
                'vy': random.randint(-8, -2),
                'size': random.randint(3, 8),
                'color': self.RED
            }
            self.health_bar_fragments.append(fragment)
    
    def update_death_animation(self):
        """사망 애니메이션 업데이트"""
        self.animation_frame += 1
        
        # 파편들 업데이트
        for fragment in self.health_bar_fragments:
            fragment['x'] += fragment['vx']
            fragment['y'] += fragment['vy']
            fragment['vy'] += 0.3  # 중력 효과
        
        # 애니메이션 완료 확인
        if self.animation_frame >= self.animation_duration:
            self.state = GameState.GAME_OVER
            print("애니메이션 완료! 게임 오버.")
    
    def get_animation_progress(self) -> float:
        """애니메이션 진행률 반환 (0.0 ~ 1.0)"""
        return min(1.0, self.animation_frame / self.animation_duration)
