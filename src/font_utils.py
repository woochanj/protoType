#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
한글 폰트 관리 유틸리티
"""

import pygame
import os
import sys

def get_korean_font(size: int) -> pygame.font.Font:
    """한글 폰트를 로드합니다."""
    
    # Windows에서 사용 가능한 한글 폰트 목록
    korean_fonts = [
        "Malgun Gothic",      # 맑은 고딕
        "Nanum Gothic",       # 나눔고딕
        "Dotum",              # 돋움
        "Gulim",              # 굴림
        "Batang",             # 바탕
        "Arial Unicode MS",   # Arial Unicode
        "Microsoft YaHei",    # 마이크로소프트 야헤이
    ]
    
    # 폰트 로드 시도
    for font_name in korean_fonts:
        try:
            font = pygame.font.SysFont(font_name, size)
            # 테스트: 한글 문자 렌더링 가능한지 확인
            test_surface = font.render("가", True, (255, 255, 255))
            if test_surface.get_width() > 0:
                return font
        except:
            continue
    
    # 시스템 폰트로도 실패하면 기본 폰트 사용
    try:
        return pygame.font.Font(None, size)
    except:
        # 최후의 수단: 기본 폰트
        return pygame.font.SysFont("arial", size)

def get_font_with_fallback(size: int, fallback_size: int = None) -> pygame.font.Font:
    """폰트를 로드하고 실패 시 fallback 폰트를 사용합니다."""
    if fallback_size is None:
        fallback_size = size
    
    try:
        return get_korean_font(size)
    except:
        try:
            return pygame.font.Font(None, fallback_size)
        except:
            return pygame.font.SysFont("arial", fallback_size)

def render_text_safe(font: pygame.font.Font, text: str, color: tuple) -> pygame.Surface:
    """안전하게 텍스트를 렌더링합니다."""
    try:
        return font.render(text, True, color)
    except:
        # 한글이 깨지면 영어로 표시
        english_text = text.replace("가위", "Scissors").replace("바위", "Rock").replace("보", "Paper")
        english_text = english_text.replace("플레이어", "Player").replace("컴퓨터", "Computer")
        english_text = english_text.replace("승리", "Win").replace("무승부", "Draw")
        english_text = english_text.replace("데미지", "Damage").replace("체력", "HP")
        english_text = english_text.replace("라운드", "Round").replace("게임 오버", "Game Over")
        english_text = english_text.replace("확인", "OK").replace("다음 라운드", "Next Round")
        english_text = english_text.replace("재시작", "Restart")
        
        return font.render(english_text, True, color)
