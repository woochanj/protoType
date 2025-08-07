#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
심리전 가위바위보 AI 플레이어 클래스
"""

import random
from typing import List, Dict, Optional
from collections import deque
from .player import Player, Choice

class AIPlayer(Player):
    def __init__(self, name: str, x: int, y: int):
        """AI 플레이어 초기화"""
        super().__init__(name, x, y)
        
        # 패턴 분석을 위한 데이터
        self.player_history = deque(maxlen=10)  # 플레이어의 최근 10개 선택
        self.ai_history = deque(maxlen=10)      # AI의 최근 10개 선택
        self.round_results = deque(maxlen=10)   # 최근 10라운드 결과
        
        # 패턴 분석 가중치
        self.pattern_weights = {
            'recent_choice': 0.4,      # 최근 선택 패턴
            'win_after_choice': 0.3,   # 승리 후 선택 패턴
            'lose_after_choice': 0.2,  # 패배 후 선택 패턴
            'random': 0.1              # 랜덤 요소
        }
        
        # AI 난이도 (0.0 ~ 1.0)
        self.difficulty = 0.7
        
        # 패턴 분석 메시지
        self.analysis_message = ""
    
    def record_player_choice(self, choice: Choice):
        """플레이어 선택 기록"""
        self.player_history.append(choice)
    
    def record_ai_choice(self, choice: Choice):
        """AI 선택 기록"""
        self.ai_history.append(choice)
    
    def record_round_result(self, player_choice: Choice, ai_choice: Choice, winner: Optional[Player]):
        """라운드 결과 기록"""
        result = {
            'player_choice': player_choice,
            'ai_choice': ai_choice,
            'winner': winner
        }
        self.round_results.append(result)
    
    def analyze_recent_pattern(self) -> Dict[Choice, float]:
        """최근 선택 패턴 분석"""
        if len(self.player_history) < 3:
            return {choice: 1/3 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        # 최근 3개 선택 분석
        recent_choices = list(self.player_history)[-3:]
        choice_counts = {choice: 0 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        for choice in recent_choices:
            choice_counts[choice] += 1
        
        # 확률 계산
        total = len(recent_choices)
        probabilities = {choice: count/total for choice, count in choice_counts.items()}
        
        return probabilities
    
    def analyze_win_pattern(self) -> Dict[Choice, float]:
        """승리 후 선택 패턴 분석"""
        if len(self.round_results) < 2:
            return {choice: 1/3 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        # 플레이어가 승리한 라운드들 찾기 (AI가 패배한 라운드)
        win_rounds = [result for result in self.round_results if result['winner'] is not None and result['winner'].name == "플레이어"]
        
        if len(win_rounds) < 2:
            return {choice: 1/3 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        # 승리 후 다음 선택 분석
        next_choices = []
        for i, result in enumerate(win_rounds[:-1]):
            if i + 1 < len(self.player_history):
                next_choices.append(self.player_history[i + 1])
        
        if not next_choices:
            return {choice: 1/3 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        choice_counts = {choice: 0 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        for choice in next_choices:
            choice_counts[choice] += 1
        
        total = len(next_choices)
        probabilities = {choice: count/total for choice, count in choice_counts.items()}
        
        return probabilities
    
    def analyze_lose_pattern(self) -> Dict[Choice, float]:
        """패배 후 선택 패턴 분석"""
        if len(self.round_results) < 2:
            return {choice: 1/3 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        # 플레이어가 패배한 라운드들 찾기 (AI가 승리한 라운드)
        lose_rounds = [result for result in self.round_results if result['winner'] is not None and result['winner'].name == "컴퓨터"]
        
        if len(lose_rounds) < 2:
            return {choice: 1/3 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        # 패배 후 다음 선택 분석
        next_choices = []
        for i, result in enumerate(lose_rounds[:-1]):
            if i + 1 < len(self.player_history):
                next_choices.append(self.player_history[i + 1])
        
        if not next_choices:
            return {choice: 1/3 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        choice_counts = {choice: 0 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        for choice in next_choices:
            choice_counts[choice] += 1
        
        total = len(next_choices)
        probabilities = {choice: count/total for choice, count in choice_counts.items()}
        
        return probabilities
    
    def predict_player_choice(self) -> Dict[Choice, float]:
        """플레이어의 다음 선택 예측"""
        # 각 패턴 분석
        recent_pattern = self.analyze_recent_pattern()
        win_pattern = self.analyze_win_pattern()
        lose_pattern = self.analyze_lose_pattern()
        
        # 가중 평균 계산
        final_probabilities = {choice: 0.0 for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]}
        
        for choice in [Choice.SCISSORS, Choice.ROCK, Choice.PAPER]:
            prob = (recent_pattern[choice] * self.pattern_weights['recent_choice'] +
                   win_pattern[choice] * self.pattern_weights['win_after_choice'] +
                   lose_pattern[choice] * self.pattern_weights['lose_after_choice'] +
                   (1/3) * self.pattern_weights['random'])
            final_probabilities[choice] = prob
        
        return final_probabilities
    
    def choose_counter_strategy(self, predicted_choice: Choice) -> Choice:
        """예측된 선택에 대한 대응 전략"""
        # 상성 규칙에 따른 대응
        counter_map = {
            Choice.SCISSORS: Choice.ROCK,    # 가위 -> 바위
            Choice.ROCK: Choice.PAPER,       # 바위 -> 보
            Choice.PAPER: Choice.SCISSORS    # 보 -> 가위
        }
        return counter_map[predicted_choice]
    
    def make_choice(self) -> Choice:
        """AI가 선택하기"""
        if len(self.player_history) < 2:
            # 데이터가 부족하면 랜덤 선택
            self.analysis_message = "데이터 부족으로 랜덤 선택"
            return random.choice([Choice.SCISSORS, Choice.ROCK, Choice.PAPER])
        
        # 플레이어 선택 예측
        prediction = self.predict_player_choice()
        predicted_choice = max(prediction, key=prediction.get)
        
        # 난이도에 따른 결정
        if random.random() < self.difficulty:
            # 패턴 분석 기반 선택
            counter_choice = self.choose_counter_strategy(predicted_choice)
            self.analysis_message = f"플레이어가 {predicted_choice.value}를 선택할 것으로 예상하여 {counter_choice.value}로 대응"
            return counter_choice
        else:
            # 랜덤 선택
            self.analysis_message = "랜덤 선택"
            return random.choice([Choice.SCISSORS, Choice.ROCK, Choice.PAPER])
    
    def get_analysis_message(self) -> str:
        """분석 메시지 반환"""
        return self.analysis_message
    
    def set_difficulty(self, difficulty: float):
        """AI 난이도 설정 (0.0 ~ 1.0)"""
        self.difficulty = max(0.0, min(1.0, difficulty))
    
    def get_difficulty(self) -> float:
        """AI 난이도 반환"""
        return self.difficulty
