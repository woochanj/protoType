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
from .font_utils import get_korean_font

class GameState(Enum):
    SETUP = "데미지 배분"
    PLAYING = "게임 진행"
    ROUND_RESULT = "라운드 결과"
    GAME_OVER = "게임 종료"

class GameManager:
    def __init__(self):
        """게임 매니저 초기화"""
        self.state = GameState.SETUP
        self.player = Player("플레이어", 50, 100)
        self.computer = Player("컴퓨터", 550, 100)
        
        # 라운드 정보
        self.round_number = 1
        self.round_result = None
        self.round_damage = 0
        
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
        return winner.damage_allocation[choice]
    
    def process_round(self):
        """라운드 처리"""
        player_choice = self.player.get_choice()
        computer_choice = self.computer.get_choice()
        
        if player_choice is None or computer_choice is None:
            return
        
        winner = self.get_winner(player_choice, computer_choice)
        
        if winner:
            damage = self.calculate_damage(winner, winner.get_choice())
            loser = self.computer if winner == self.player else self.player
            loser.take_damage(damage)
            self.round_damage = damage
        else:
            self.round_damage = 0
        
        self.round_result = {
            'player_choice': player_choice,
            'computer_choice': computer_choice,
            'winner': winner,
            'damage': self.round_damage
        }
        
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
        # 간단한 AI: 랜덤 선택
        choices = [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]
        choice = random.choice(choices)
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
        self.state = GameState.SETUP
        self.setup_computer_damage()
