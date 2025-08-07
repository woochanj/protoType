#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
심리전 가위바위보 플레이어 클래스
"""

import pygame
from typing import Tuple, Dict
from enum import Enum
from .font_utils import get_korean_font, render_text_safe

class Choice(Enum):
    ROCK = "바위"
    PAPER = "보"
    SCISSORS = "가위"

class Player:
    def __init__(self, name: str, x: int, y: int):
        """플레이어 초기화"""
        self.name = name
        self.x = x
        self.y = y
        self.max_health = 20
        self.health = self.max_health
        
        # 데미지 배분 (가위, 바위, 보)
        self.damage_allocation = {
            Choice.SCISSORS: 0,
            Choice.ROCK: 0,
            Choice.PAPER: 0
        }
        
        # 현재 선택
        self.current_choice = None
        
        # 특수 능력 관련
        self.consecutive_choices = 0  # 연속 같은 선택 횟수
        self.last_choice = None       # 이전 선택
        self.special_ability_active = False  # 특수 능력 활성화 여부
        self.defense_bonus = False    # 방어 보너스 (바위 특수 능력)
        
        # 연속 보너스 관련
        self.consecutive_wins = 0     # 연속 승리 횟수
        self.consecutive_losses = 0   # 연속 패배 횟수
        self.bonus_damage = 0         # 보너스 데미지
        
        # 색상
        self.color = (0, 255, 0) if name == "플레이어" else (255, 0, 0)
        self.health_color = (255, 255, 0)
        
        # UI 요소 - 한글 폰트 사용
        self.font = get_korean_font(24)
        self.small_font = get_korean_font(18)
    
    def set_damage_allocation(self, scissors: int, rock: int, paper: int):
        """데미지 배분 설정"""
        total = scissors + rock + paper
        if total > 20:
            raise ValueError("데미지 총합이 20을 초과할 수 없습니다!")
        
        self.damage_allocation[Choice.SCISSORS] = scissors
        self.damage_allocation[Choice.ROCK] = rock
        self.damage_allocation[Choice.PAPER] = paper
    
    def get_damage_allocation(self) -> Dict[Choice, int]:
        """데미지 배분 반환"""
        return self.damage_allocation.copy()
    
    def get_damage_allocation_tuple(self) -> Tuple[int, int, int]:
        """데미지 배분을 튜플로 반환 (가위, 바위, 보 순서)"""
        return (self.damage_allocation[Choice.SCISSORS],
                self.damage_allocation[Choice.ROCK],
                self.damage_allocation[Choice.PAPER])
    
    def set_choice(self, choice: Choice):
        """선택 설정"""
        # 연속 선택 체크
        if self.last_choice == choice:
            self.consecutive_choices += 1
        else:
            self.consecutive_choices = 1
        
        self.last_choice = choice
        self.current_choice = choice
        
        # 특수 능력 체크
        self.check_special_ability()
    
    def check_special_ability(self):
        """특수 능력 체크"""
        if self.consecutive_choices >= 2:
            self.special_ability_active = True
        else:
            self.special_ability_active = False
    
    def get_choice(self) -> Choice:
        """현재 선택 반환"""
        return self.current_choice
    
    def take_damage(self, damage: int):
        """데미지 받기"""
        # 방어 보너스 적용
        if self.defense_bonus:
            damage = max(1, damage // 2)  # 데미지 절반으로 감소 (최소 1)
            self.defense_bonus = False  # 한 번만 적용
        
        self.health = max(0, self.health - damage)
    
    def is_alive(self) -> bool:
        """생존 여부 확인"""
        return self.health > 0
    
    def get_health_percentage(self) -> float:
        """체력 백분율 반환"""
        return self.health / self.max_health
    
    def reset_choice(self):
        """선택 초기화"""
        self.current_choice = None
        # 특수 능력은 유지 (다음 라운드까지)
    
    def apply_rock_special_ability(self):
        """바위 특수 능력 적용 (방어 보너스)"""
        self.defense_bonus = True
    
    def get_special_ability_damage_multiplier(self) -> float:
        """특수 능력 데미지 배율 반환"""
        if not self.special_ability_active:
            return 1.0
        
        # 가위: 연속 공격 (1.5배)
        if self.current_choice == Choice.SCISSORS:
            return 1.5
        # 보: 복사 능력 (기본 1.0배, 하지만 다른 효과)
        elif self.current_choice == Choice.PAPER:
            return 1.0
        # 바위: 방어 능력 (기본 1.0배, 하지만 데미지 감소)
        else:
            return 1.0
    
    def record_win(self):
        """승리 기록"""
        self.consecutive_wins += 1
        self.consecutive_losses = 0
        
        # 3연속 승리 보너스
        if self.consecutive_wins >= 3:
            self.bonus_damage = 1.5
    
    def record_loss(self):
        """패배 기록"""
        self.consecutive_losses += 1
        self.consecutive_wins = 0
        
        # 3연속 패배 보너스 (다음 승리 시 2배 데미지)
        if self.consecutive_losses >= 3:
            self.bonus_damage = 2.0
    
    def get_bonus_damage_multiplier(self) -> float:
        """보너스 데미지 배율 반환"""
        return self.bonus_damage if self.bonus_damage > 0 else 1.0
    
    def reset_bonus_damage(self):
        """보너스 데미지 리셋"""
        self.bonus_damage = 0
    
    def draw(self, screen, show_damage_allocation: bool = False):
        """플레이어 그리기"""
        # 이름 표시
        name_text = render_text_safe(self.font, self.name, self.color)
        screen.blit(name_text, (self.x, self.y))
        
        # 체력 바
        bar_width = 200
        bar_height = 20
        bar_x = self.x
        bar_y = self.y + 30
        
        # 배경 (회색)
        pygame.draw.rect(screen, (100, 100, 100), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # 체력 (노란색)
        health_width = int(bar_width * self.get_health_percentage())
        pygame.draw.rect(screen, self.health_color, 
                        (bar_x, bar_y, health_width, bar_height))
        
        # 테두리
        pygame.draw.rect(screen, (255, 255, 255), 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # 체력 텍스트
        health_text = render_text_safe(self.small_font, f"{self.health}/{self.max_health}", (255, 255, 255))
        screen.blit(health_text, (bar_x + bar_width + 10, bar_y))
        
        # 데미지 배분 표시 (옵션)
        if show_damage_allocation:
            y_offset = 60
            for choice, damage in self.damage_allocation.items():
                damage_text = render_text_safe(self.small_font, f"{choice.value}: {damage}", (255, 255, 255))
                screen.blit(damage_text, (self.x, self.y + y_offset))
                y_offset += 20
        
        # 현재 선택 표시
        if self.current_choice:
            choice_text = render_text_safe(self.font, f"선택: {self.current_choice.value}", (255, 255, 0))
            screen.blit(choice_text, (self.x, self.y + 120))
    
    def get_total_damage(self) -> int:
        """총 데미지 반환"""
        return sum(self.damage_allocation.values())
