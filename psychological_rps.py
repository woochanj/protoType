#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
심리전 가위바위보 게임
"""

import pygame
import sys
from src.player import Choice
from src.game_manager import GameManager, GameState
from src.ui import UI

class PsychologicalRPS:
    def __init__(self, width: int = 800, height: int = 600):
        """게임 초기화"""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("심리전 가위바위보")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # 게임 매니저와 UI
        self.game_manager = GameManager()
        self.ui = UI(width, height)
        
        # 색상
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        
        print("심리전 가위바위보 게임이 시작되었습니다!")
        print("게임 규칙:")
        print("1. 게임 시작 전 가위, 바위, 보에 데미지를 배분하세요 (총합 20)")
        print("2. 매 라운드 가위바위보를 선택하세요")
        print("3. 승자는 자신이 할당한 데미지만큼 상대방 체력을 깎습니다")
        print("4. 체력이 0이 되면 패배합니다")
    
    def handle_events(self):
        """이벤트 처리"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # 마우스 이벤트 처리
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        action = self.ui.handle_mouse(mouse_pos, mouse_click)
        if action:
            self.handle_action(action)
    
    def handle_action(self, action: str):
        """액션 처리"""
        if action == "confirm_setup":
            self.handle_setup_confirmation()
        elif action == "choose_scissors":
            self.handle_choice(Choice.SCISSORS)
        elif action == "choose_rock":
            self.handle_choice(Choice.ROCK)
        elif action == "choose_paper":
            self.handle_choice(Choice.PAPER)
        elif action == "next_round":
            self.handle_next_round()
        elif action == "restart":
            self.handle_restart()
    
    def handle_setup_confirmation(self):
        """데미지 배분 확인 처리"""
        if self.ui.is_valid_allocation():
            scissors, rock, paper = self.ui.get_damage_allocation()
            self.game_manager.player.set_damage_allocation(scissors, rock, paper)
            self.game_manager.set_state(GameState.PLAYING)
            print(f"데미지 배분 완료: 가위 {scissors}, 바위 {rock}, 보 {paper}")
        else:
            print("데미지 총합이 20이어야 합니다!")
    
    def handle_choice(self, choice: Choice):
        """선택 처리"""
        if self.game_manager.get_state() == GameState.PLAYING:
            self.game_manager.player.set_choice(choice)
            print(f"플레이어 선택: {choice.value}")
            
            # 컴퓨터 선택
            self.game_manager.computer_choose()
            print(f"컴퓨터 선택: {self.game_manager.computer.get_choice().value}")
            
            # 라운드 처리
            self.game_manager.process_round()
            
            # 게임 오버 확인
            if self.game_manager.check_game_over():
                winner = self.game_manager.get_winner_player()
                if winner:
                    print(f"게임 종료! {winner.name} 승리!")
                else:
                    print("게임 종료!")
    
    def handle_next_round(self):
        """다음 라운드 처리"""
        if self.game_manager.get_state() == GameState.ROUND_RESULT:
            self.game_manager.next_round()
            print(f"라운드 {self.game_manager.round_number} 시작!")
    
    def handle_restart(self):
        """게임 재시작 처리"""
        self.game_manager.reset_game()
        print("게임이 재시작되었습니다!")
    
    def update(self):
        """게임 업데이트"""
        pass
    
    def draw(self):
        """화면 그리기"""
        # 배경
        self.screen.fill(self.BLACK)
        
        # 게임 상태에 따른 화면 그리기
        state = self.game_manager.get_state()
        
        if state == GameState.SETUP:
            self.ui.draw_setup_screen(self.screen, self.game_manager.player)
        elif state == GameState.PLAYING:
            self.ui.draw_game_screen(self.screen, self.game_manager)
        elif state == GameState.ROUND_RESULT:
            self.ui.draw_result_screen(self.screen, self.game_manager)
        elif state == GameState.GAME_OVER:
            self.ui.draw_game_over_screen(self.screen, self.game_manager)
        
        # 화면 업데이트
        pygame.display.flip()
    
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
    game = PsychologicalRPS(800, 600)
    game.run()

if __name__ == "__main__":
    main()
