#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
农业AI后端服务主程序
提供作物推荐、病虫害识别等AI服务接口
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 模拟机器学习模型（实际项目中应该加载训练好的模型）
class CropRecommendationModel:
    """作物推荐模型"""
    
    def __init__(self):
        self.crops = [
            '稻米', '小麦', '玉米', '大豆', '土豆',
            '番茄', '黄瓜', '胡萝卜', '白菜', '菠菜'
        ]
    
    def predict(self, features):
        """根据土壤和环境特征预测最适合的作物"""
        # 这里是简化的逻辑，实际应该使用训练好的ML模型
        n, p, k, temp, humidity, ph, rainfall = features
        
        # 简单的规则基础推荐逻辑
        if ph < 6.0:
            return '蓝莓'  # 酸性土壤
        elif ph > 7.5:
            return '苜蓿草'  # 碱性土壤
        elif temp > 25 and humidity > 80:
            return '稻米'  # 高温高湿
        elif rainfall < 100:
            return '仙人掌'  # 干旱条件
        else:
            return np.random.choice(self.crops)

class SoilQualityModel:
    """土壤质量评估模型"""
    
    def assess_quality(self, features):
        """评估土壤质量"""
        n, p, k, ph, organic_matter = features
        
        # 计算综合评分
        score = 0
        
        # pH评分
        if 6.0 <= ph <= 7.0:
            score += 25
        elif 5.5 <= ph <= 7.5:
            score += 20
        else:
            score += 10
            
        # 营养成分评分
        if n > 50: score += 25
        elif n > 30: score += 20
        else: score += 10
        
        if p > 30: score += 25
        elif p > 20: score += 20
        else: score += 10
        
        if k > 40: score += 25
        elif k > 25: score += 20
        else: score += 10
        
        # 有机物含量评分
        if organic_matter > 3: score += 25
        elif organic_matter > 2: score += 20
        else: score += 10
        
        if score >= 90:
            return '优秀', score
        elif score >= 70:
            return '良好', score
        elif score >= 50:
            return '一般', score
        else:
            return '较差', score

# 初始化模型
crop_model = CropRecommendationModel()
soil_model = SoilQualityModel()

@app.route('/')
def home():
    """API根路径"""
    return jsonify({
        'message': '欢迎使用农业AI智能决策系统',
        'version': '1.0.0',
        'endpoints': [
            '/api/crop-recommendation',
            '/api/soil-quality',
            '/api/weather-forecast',
            '/api/disease-detection'
        ],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/crop-recommendation', methods=['POST'])
def crop_recommendation():
    """作物推荐接口"""
    try:
        data = request.get_json()
        
        # 验证输入参数
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 
                          'temperature', 'humidity', 'ph', 'rainfall']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必需参数: {field}'}), 400
        
        # 提取特征
        features = [
            float(data['nitrogen']),
            float(data['phosphorus']),
            float(data['potassium']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]
        
        # 预测推荐作物
        recommended_crop = crop_model.predict(features)
        
        # 生成建议
        suggestions = generate_crop_suggestions(features, recommended_crop)
        
        return jsonify({
            'recommended_crop': recommended_crop,
            'confidence': np.random.uniform(0.7, 0.95),  # 模拟置信度
            'suggestions': suggestions,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/soil-quality', methods=['POST'])
def soil_quality_assessment():
    """土壤质量评估接口"""
    try:
        data = request.get_json()
        
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'ph', 'organic_matter']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必需参数: {field}'}), 400
        
        features = [
            float(data['nitrogen']),
            float(data['phosphorus']),
            float(data['potassium']),
            float(data['ph']),
            float(data['organic_matter'])
        ]
        
        quality, score = soil_model.assess_quality(features)
        
        recommendations = generate_soil_recommendations(features)
        
        return jsonify({
            'quality_level': quality,
            'score': score,
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_crop_suggestions(features, crop):
    """生成作物种植建议"""
    suggestions = []
    
    n, p, k, temp, humidity, ph, rainfall = features
    
    if ph < 6.0:
        suggestions.append('土壤偏酸，建议施用石灰调节pH值')
    elif ph > 7.5:
        suggestions.append('土壤偏碱，建议施用硫磺或有机肥调节pH值')
    
    if n < 40:
        suggestions.append('氮含量较低，建议增施氮肥')
    
    if p < 20:
        suggestions.append('磷含量不足，建议施用磷肥')
    
    if k < 30:
        suggestions.append('钾含量偏低，建议补充钾肥')
    
    if rainfall < 100:
        suggestions.append('降雨量较少，需要加强灌溉管理')
    
    return suggestions

def generate_soil_recommendations(features):
    """生成土壤改良建议"""
    recommendations = []
    
    n, p, k, ph, organic_matter = features
    
    if organic_matter < 2:
        recommendations.append('有机质含量偏低，建议增施有机肥或堆肥')
    
    if n < 30:
        recommendations.append('氮素缺乏，建议施用氮肥如尿素或硫酸铵')
    
    if p < 20:
        recommendations.append('磷素不足，建议施用过磷酸钙或磷酸二铵')
    
    if k < 25:
        recommendations.append('钾素缺乏，建议施用氯化钾或硫酸钾')
    
    return recommendations

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)