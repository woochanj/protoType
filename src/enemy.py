#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
적 클래스
게임의 적 캐릭터를 관리합니다.
"""

import pygame
import random
from typing import Tuple, List

class Enemy:
    def __init__(self, x: int, y: int, width: int = 24, height: int = 24):
        """적 초기화"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 2
        self.color = (255, 0, 0)  # 빨간색
        
        # 적의 사각형 (충돌 감지용)
        self.rect = pygame.Rect(x, y, width, height)
        
        # AI 관련 변수들
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.change_direction_timer = 0
        self.change_direction_interval = 60  # 1초마다 방향 변경 (60 FPS 기준)
        
        # 상태
        self.active = True
    
    def update(self, screen_width: int, screen_height: int, player_pos: Tuple[int, int]):
        """적 업데이트"""
        if not self.active:
            return
        
        # 방향 변경 타이머 업데이트
        self.change_direction_timer += 1
        if self.change_direction_timer >= self.change_direction_interval:
            self.change_direction_timer = 0
            self.change_direction()
        
        # 이동 처리
        dx, dy = self.direction
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # 화면 경계 체크
        if new_x < 0 or new_x > screen_width - self.width:
            self.direction = (-dx, dy)
            new_x = self.x
        if new_y < 0 or new_y > screen_height - self.height:
            self.direction = (dx, -dy)
            new_y = self.y
        
        self.x = new_x
        self.y = new_y
        
        # 사각형 위치 업데이트
        self.rect.x = self.x
        self.rect.y = self.y
    
    def change_direction(self):
        """방향 변경"""
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        self.direction = random.choice(directions)
    
    def draw(self, screen):
        """적 그리기"""
        if not self.active:
            return
        
        pygame.draw.rect(screen, self.color, self.rect)
        
        # 적 중심점 표시 (디버깅용)
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), 2)
    
    def get_position(self) -> Tuple[int, int]:
        """적 위치 반환"""
        return (self.x, self.y)
    
    def get_center(self) -> Tuple[int, int]:
        """적 중심점 반환"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def set_position(self, x: int, y: int):
        """적 위치 설정"""
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
    
    def check_collision(self, other_rect: pygame.Rect) -> bool:
        """다른 오브젝트와의 충돌 감지"""
        return self.rect.colliderect(other_rect)
    
    def deactivate(self):
        """적 비활성화"""
        self.active = False
    
    def activate(self):
        """적 활성화"""
        self.active = True

class EnemyManager:
    def __init__(self):
        """적 관리자 초기화"""
        self.enemies: List[Enemy] = []
    
    def add_enemy(self, x: int, y: int):
        """적 추가"""
        enemy = Enemy(x, y)
        self.enemies.append(enemy)
    
    def add_enemies_random(self, count: int, screen_width: int, screen_height: int):
        """랜덤 위치에 적들 추가"""
        for _ in range(count):
            x = random.randint(0, screen_width - 24)
            y = random.randint(0, screen_height - 24)
            self.add_enemy(x, y)
    
    def update(self, screen_width: int, screen_height: int, player_pos: Tuple[int, int]):
        """모든 적 업데이트"""
        for enemy in self.enemies:
            enemy.update(screen_width, screen_height, player_pos)
    
    def draw(self, screen):
        """모든 적 그리기"""
        for enemy in self.enemies:
            enemy.draw(screen)
    
    def check_collisions(self, player_rect: pygame.Rect) -> List[Enemy]:
        """플레이어와 충돌하는 적들 반환"""
        colliding_enemies = []
        for enemy in self.enemies:
            if enemy.active and enemy.check_collision(player_rect):
                colliding_enemies.append(enemy)
        return colliding_enemies
    
    def remove_inactive_enemies(self):
        """비활성화된 적들 제거"""
        self.enemies = [enemy for enemy in self.enemies if enemy.active]
    
    def get_active_enemies(self) -> List[Enemy]:
        """활성화된 적들 반환"""
        return [enemy for enemy in self.enemies if enemy.active]
