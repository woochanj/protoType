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
    
    def set_choice(self, choice: Choice):
        """선택 설정"""
        self.current_choice = choice
    
    def get_choice(self) -> Choice:
        """현재 선택 반환"""
        return self.current_choice
    
    def take_damage(self, damage: int):
        """데미지 받기"""
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
