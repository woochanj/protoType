#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
파이썬 게임 개발 프로젝트
기본 게임 루프와 pygame 설정
"""

import pygame
import sys
from typing import Tuple

class Game:
    def __init__(self, width: int = 800, height: int = 600, title: str = "파이썬 게임"):
        """게임 초기화"""
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # 색상 정의
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
        print(f"게임이 시작되었습니다: {title}")
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                self.on_keydown(event)
            elif event.type == pygame.KEYUP:
                self.on_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_mouse_click(event)
    
    def on_keydown(self, event):
        """키 다운 이벤트 처리 (오버라이드 가능)"""
        pass
    
    def on_keyup(self, event):
        """키 업 이벤트 처리 (오버라이드 가능)"""
        pass
    
    def on_mouse_click(self, event):
        """마우스 클릭 이벤트 처리 (오버라이드 가능)"""
        pass
    
    def update(self):
        """게임 로직 업데이트 (오버라이드 가능)"""
        pass
    
    def draw(self):
        """화면 그리기 (오버라이드 가능)"""
        # 기본 배경색
        self.screen.fill(self.BLACK)
        
        # 여기에 게임 오브젝트들을 그리세요
        # 예시: 화면 중앙에 빨간 원 그리기
        pygame.draw.circle(self.screen, self.RED, 
                          (self.width // 2, self.height // 2), 50)
        
        # 화면 업데이트
        pygame.display.flip()
    
    def run(self):
        """메인 게임 루프"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
        
        self.quit()
    
    def quit(self):
        """게임 종료"""
        pygame.quit()
        sys.exit()

def main():
    """메인 함수"""
    game = Game(800, 600, "파이썬 게임 개발")
    game.run()

if __name__ == "__main__":
    main()
