#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
완전한 게임 예제
플레이어와 적이 포함된 기본 게임
"""

import pygame
import sys
from src.player import Player
from src.enemy import EnemyManager

class ExampleGame:
    def __init__(self, width: int = 800, height: int = 600):
        """게임 초기화"""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("파이썬 게임 예제")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # 색상 정의
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        # 게임 오브젝트들
        self.player = Player(width // 2, height // 2)
        self.enemy_manager = EnemyManager()
        
        # 게임 상태
        self.score = 0
        self.game_over = False
        self.font = pygame.font.Font(None, 36)
        
        # 적 생성
        self.enemy_manager.add_enemies_random(5, width, height)
        
        print("게임이 시작되었습니다!")
        print("조작법: WASD 또는 화살표 키로 이동")
        print("ESC: 게임 종료")
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
    
    def update(self):
        """게임 로직 업데이트"""
        if self.game_over:
            return
        
        # 키보드 입력 처리
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # 플레이어 업데이트
        self.player.update(self.width, self.height)
        
        # 적 업데이트
        self.enemy_manager.update(self.width, self.height, self.player.get_position())
        
        # 충돌 감지
        colliding_enemies = self.enemy_manager.check_collisions(self.player.rect)
        for enemy in colliding_enemies:
            enemy.deactivate()
            self.score += 10
        
        # 비활성화된 적들 제거
        self.enemy_manager.remove_inactive_enemies()
        
        # 모든 적이 제거되면 새로운 적들 생성
        if len(self.enemy_manager.get_active_enemies()) == 0:
            self.enemy_manager.add_enemies_random(5, self.width, self.height)
    
    def draw(self):
        """화면 그리기"""
        # 배경 그리기
        self.screen.fill(self.BLACK)
        
        # 플레이어 그리기
        self.player.draw(self.screen)
        
        # 적들 그리기
        self.enemy_manager.draw(self.screen)
        
        # 점수 표시
        score_text = self.font.render(f"점수: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 게임 오버 화면
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_game_over(self):
        """게임 오버 화면 그리기"""
        # 반투명 오버레이
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill(self.BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # 게임 오버 텍스트
        game_over_text = self.font.render("게임 오버!", True, self.RED)
        restart_text = self.font.render("R 키를 눌러 재시작", True, self.WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        restart_rect = restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """게임 재시작"""
        self.player.set_position(self.width // 2, self.height // 2)
        self.enemy_manager = EnemyManager()
        self.enemy_manager.add_enemies_random(5, self.width, self.height)
        self.score = 0
        self.game_over = False
    
    def run(self):
        """메인 게임 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

def main():
    """메인 함수"""
    game = ExampleGame(800, 600)
    game.run()

if __name__ == "__main__":
    main()
