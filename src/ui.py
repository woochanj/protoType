#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
심리전 가위바위보 UI 관리
"""

import pygame
from typing import Tuple, Optional, List
from .player import Choice
from .game_manager import GameState
from .font_utils import get_korean_font, render_text_safe

class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int]):
        """버튼 초기화"""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(255, c + 30) for c in color)
        self.is_hovered = False
        self.font = get_korean_font(24)
    
    def draw(self, screen):
        """버튼 그리기"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        text_surface = render_text_safe(self.font, self.text, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_mouse(self, pos: Tuple[int, int]):
        """마우스 이벤트 처리"""
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos: Tuple[int, int], click: bool) -> bool:
        """클릭 확인"""
        return self.rect.collidepoint(pos) and click

class Slider:
    def __init__(self, x: int, y: int, width: int, height: int, min_val: int, max_val: int, initial_val: int, name: str = ""):
        """슬라이더 초기화"""
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.name = name
        self.is_dragging = False
        self.font = get_korean_font(20)
    
    def draw(self, screen):
        """슬라이더 그리기"""
        # 배경
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # 슬라이더 핸들
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, (255, 255, 0), handle_rect)
        
        # 값 표시
        value_text = render_text_safe(self.font, str(self.value), (255, 255, 255))
        screen.blit(value_text, (self.rect.x + self.rect.width + 10, self.rect.y))
    
    def handle_mouse(self, pos: Tuple[int, int], click: bool):
        """마우스 이벤트 처리"""
        if click and self.rect.collidepoint(pos):
            self.is_dragging = True
        
        if not click:
            self.is_dragging = False
        
        if self.is_dragging:
            rel_x = pos[0] - self.rect.x
            ratio = max(0, min(1, rel_x / self.rect.width))
            new_value = int(self.min_val + ratio * (self.max_val - self.min_val))
            return new_value
        
        return None

class LinkedSliders:
    def __init__(self, max_total: int = 20):
        """연동된 슬라이더 그룹"""
        self.max_total = max_total
        self.sliders = {}
        self.setup_sliders()
    
    def setup_sliders(self):
        """슬라이더 설정"""
        self.sliders['scissors'] = Slider(200, 200, 150, 20, 0, 20, 0, "가위")
        self.sliders['rock'] = Slider(200, 230, 150, 20, 0, 20, 0, "바위")
        self.sliders['paper'] = Slider(200, 260, 150, 20, 0, 20, 0, "보")
    
    def get_total(self) -> int:
        """총합 계산"""
        return sum(slider.value for slider in self.sliders.values())
    
    def adjust_sliders(self, changed_slider_name: str, new_value: int):
        """슬라이더 값 조정"""
        # 변경된 슬라이더의 값 설정
        self.sliders[changed_slider_name].value = new_value
        
        # 총합 계산
        total = self.get_total()
        
        # 총합이 최대값을 초과하면 다른 슬라이더들 조정
        if total > self.max_total:
            excess = total - self.max_total
            
            # 변경되지 않은 슬라이더들 찾기
            other_sliders = [name for name in self.sliders.keys() if name != changed_slider_name]
            
            # 큰 값부터 줄이기
            other_sliders.sort(key=lambda name: self.sliders[name].value, reverse=True)
            
            # 초과분만큼 줄이기
            for name in other_sliders:
                if excess <= 0:
                    break
                
                current_value = self.sliders[name].value
                reduction = min(excess, current_value)
                self.sliders[name].value -= reduction
                excess -= reduction
    
    def handle_mouse(self, pos: Tuple[int, int], click: bool) -> Optional[str]:
        """마우스 이벤트 처리"""
        for name, slider in self.sliders.items():
            new_value = slider.handle_mouse(pos, click)
            if new_value is not None:
                self.adjust_sliders(name, new_value)
                return name
        return None
    
    def draw(self, screen):
        """모든 슬라이더 그리기"""
        for slider in self.sliders.values():
            slider.draw(screen)
    
    def get_values(self) -> Tuple[int, int, int]:
        """슬라이더 값들 반환 (가위, 바위, 보 순서)"""
        return (self.sliders['scissors'].value, 
                self.sliders['rock'].value, 
                self.sliders['paper'].value)
    
    def is_valid(self) -> bool:
        """유효한 배분인지 확인"""
        return self.get_total() == self.max_total

class UI:
    def __init__(self, screen_width: int, screen_height: int):
        """UI 초기화"""
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # 폰트 - 한글 폰트 사용
        self.title_font = get_korean_font(48)
        self.font = get_korean_font(36)
        self.small_font = get_korean_font(24)
        
        # 색상
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        # 버튼들
        self.setup_buttons()
        
        # 연동된 슬라이더 그룹
        self.linked_sliders = LinkedSliders(20)
    
    def setup_buttons(self):
        """버튼 설정"""
        # 데미지 배분 버튼
        self.confirm_button = Button(350, 400, 100, 40, "확인", (0, 100, 0))
        
        # 가위바위보 선택 버튼
        self.scissors_button = Button(200, 300, 80, 60, "가위", (100, 100, 100))
        self.rock_button = Button(300, 300, 80, 60, "바위", (100, 100, 100))
        self.paper_button = Button(400, 300, 80, 60, "보", (100, 100, 100))
        
        # 결과 확인 버튼
        self.next_round_button = Button(350, 450, 100, 40, "다음 라운드", (0, 100, 0))
        
        # 게임 재시작 버튼
        self.restart_button = Button(350, 500, 100, 40, "재시작", (100, 0, 0))
    
    def draw_setup_screen(self, screen, player):
        """데미지 배분 화면 그리기"""
        # 제목
        title = render_text_safe(self.title_font, "데미지 배분 (총합 20)", self.WHITE)
        screen.blit(title, (200, 50))
        
        # 설명
        desc = render_text_safe(self.font, "가위, 바위, 보에 데미지를 배분하세요", self.WHITE)
        screen.blit(desc, (150, 100))
        
        # 슬라이더 라벨들
        scissors_label = render_text_safe(self.small_font, "가위:", self.WHITE)
        rock_label = render_text_safe(self.small_font, "바위:", self.WHITE)
        paper_label = render_text_safe(self.small_font, "보:", self.WHITE)
        
        screen.blit(scissors_label, (150, 200))
        screen.blit(rock_label, (150, 230))
        screen.blit(paper_label, (150, 260))
        
        # 연동된 슬라이더들 그리기
        self.linked_sliders.draw(screen)
        
        # 총합 표시
        total = self.linked_sliders.get_total()
        total_text = render_text_safe(self.font, f"총합: {total}/20", self.YELLOW if total == 20 else self.RED)
        screen.blit(total_text, (200, 320))
        
        # 확인 버튼 (총합이 20일 때만 활성화)
        if self.linked_sliders.is_valid():
            self.confirm_button.color = (0, 100, 0)
        else:
            self.confirm_button.color = (100, 100, 100)
        
        self.confirm_button.draw(screen)
    
    def draw_game_screen(self, screen, game_manager):
        """게임 화면 그리기"""
        # 제목
        title = render_text_safe(self.title_font, f"라운드 {game_manager.round_number}", self.WHITE)
        screen.blit(title, (300, 30))
        
        # 데미지 배분 정보 표시
        damage_info = game_manager.player.get_damage_allocation_tuple()
        damage_text = render_text_safe(self.small_font, f"데미지 배분: 가위 {damage_info[0]} | 바위 {damage_info[1]} | 보 {damage_info[2]}", self.YELLOW)
        screen.blit(damage_text, (50, 80))
        

        
        # 플레이어들 그리기
        game_manager.player.draw(screen)
        game_manager.computer.draw(screen)
        
        # 선택 버튼들
        if not game_manager.player.get_choice():
            self.scissors_button.draw(screen)
            self.rock_button.draw(screen)
            self.paper_button.draw(screen)
        
        # 선택 완료 메시지
        if game_manager.player.get_choice():
            choice_text = render_text_safe(self.font, "선택 완료! 컴퓨터가 선택 중...", self.YELLOW)
            screen.blit(choice_text, (250, 400))
            
            # 특수 능력 상태 표시
            if game_manager.player.special_ability_active:
                ability_text = render_text_safe(self.small_font, f"특수 능력 활성화! (연속 {game_manager.player.consecutive_choices}회)", self.GREEN)
                screen.blit(ability_text, (50, 480))
            
            # 연속 보너스 상태 표시
            if game_manager.player.consecutive_wins >= 3:
                bonus_text = render_text_safe(self.small_font, f"연속 승리 보너스! ({game_manager.player.consecutive_wins}연속)", self.YELLOW)
                screen.blit(bonus_text, (50, 510))
            elif game_manager.player.consecutive_losses >= 3:
                bonus_text = render_text_safe(self.small_font, f"연속 패배 보너스! 다음 승리 시 2배 데미지", self.RED)
                screen.blit(bonus_text, (50, 510))
            
            # AI 분석 메시지 표시
            if hasattr(game_manager.computer, 'get_analysis_message'):
                analysis_msg = game_manager.computer.get_analysis_message()
                if analysis_msg:
                    analysis_text = render_text_safe(self.small_font, f"AI 분석: {analysis_msg}", self.BLUE)
                    screen.blit(analysis_text, (50, 450))
    
    def draw_result_screen(self, screen, game_manager):
        """결과 화면 그리기"""
        result = game_manager.round_result
        
        # 결과 제목
        if result['winner']:
            winner_name = "플레이어" if result['winner'] == game_manager.player else "컴퓨터"
            title = render_text_safe(self.title_font, f"{winner_name} 승리!", self.GREEN)
        else:
            title = render_text_safe(self.title_font, "무승부!", self.YELLOW)
        
        screen.blit(title, (300, 100))
        
        # 데미지 배분 정보 표시
        damage_info = game_manager.player.get_damage_allocation_tuple()
        damage_text = render_text_safe(self.small_font, f"데미지 배분: 가위 {damage_info[0]} | 바위 {damage_info[1]} | 보 {damage_info[2]}", self.YELLOW)
        screen.blit(damage_text, (50, 50))
        
        # 선택 표시
        player_choice = render_text_safe(self.font, f"플레이어: {result['player_choice'].value}", self.WHITE)
        computer_choice = render_text_safe(self.font, f"컴퓨터: {result['computer_choice'].value}", self.WHITE)
        
        screen.blit(player_choice, (200, 200))
        screen.blit(computer_choice, (400, 200))
        
        # 데미지 표시
        if result['damage'] > 0:
            damage_text = render_text_safe(self.font, f"데미지: {result['damage']}", self.RED)
            screen.blit(damage_text, (300, 250))
            
            # 특수 능력 데미지 표시
            winner = result['winner']
            if winner and winner.special_ability_active:
                ability_damage_text = render_text_safe(self.small_font, "특수 능력으로 데미지 증가!", self.GREEN)
                screen.blit(ability_damage_text, (300, 280))
            
            # 연속 보너스 데미지 표시
            if winner:
                if winner.consecutive_wins >= 3:
                    bonus_damage_text = render_text_safe(self.small_font, "연속 승리 보너스로 데미지 증가!", self.YELLOW)
                    screen.blit(bonus_damage_text, (300, 310))
                elif winner.consecutive_losses >= 3:
                    bonus_damage_text = render_text_safe(self.small_font, "연속 패배 보너스로 데미지 증가!", self.RED)
                    screen.blit(bonus_damage_text, (300, 310))
        
        # 다음 라운드 버튼
        self.next_round_button.draw(screen)
    
    def draw_game_over_screen(self, screen, game_manager):
        """게임 오버 화면 그리기"""
        winner = game_manager.get_winner_player()
        
        if winner:
            winner_name = "플레이어" if winner == game_manager.player else "컴퓨터"
            title = render_text_safe(self.title_font, f"{winner_name} 승리!", self.GREEN)
        else:
            title = render_text_safe(self.title_font, "게임 오버!", self.RED)
        
        screen.blit(title, (300, 150))
        
        # 데미지 배분 정보 표시
        damage_info = game_manager.player.get_damage_allocation_tuple()
        damage_text = render_text_safe(self.small_font, f"데미지 배분: 가위 {damage_info[0]} | 바위 {damage_info[1]} | 보 {damage_info[2]}", self.YELLOW)
        screen.blit(damage_text, (50, 50))
        
        # 재시작 버튼
        self.restart_button.draw(screen)
    
    def handle_mouse(self, pos: Tuple[int, int], click: bool) -> Optional[str]:
        """마우스 이벤트 처리"""
        # 모든 버튼의 호버 상태 업데이트
        self.confirm_button.handle_mouse(pos)
        self.scissors_button.handle_mouse(pos)
        self.rock_button.handle_mouse(pos)
        self.paper_button.handle_mouse(pos)
        self.next_round_button.handle_mouse(pos)
        self.restart_button.handle_mouse(pos)
        
        # 연동된 슬라이더 처리
        self.linked_sliders.handle_mouse(pos, click)
        
        # 클릭 이벤트 처리
        if click:
            if self.confirm_button.is_clicked(pos, click) and self.linked_sliders.is_valid():
                return "confirm_setup"
            elif self.scissors_button.is_clicked(pos, click):
                return "choose_scissors"
            elif self.rock_button.is_clicked(pos, click):
                return "choose_rock"
            elif self.paper_button.is_clicked(pos, click):
                return "choose_paper"
            elif self.next_round_button.is_clicked(pos, click):
                return "next_round"
            elif self.restart_button.is_clicked(pos, click):
                return "restart"
        
        return None
    
    def get_damage_allocation(self) -> Tuple[int, int, int]:
        """슬라이더에서 데미지 배분 가져오기"""
        return self.linked_sliders.get_values()
    
    def is_valid_allocation(self) -> bool:
        """데미지 배분이 유효한지 확인"""
        return self.linked_sliders.is_valid()
