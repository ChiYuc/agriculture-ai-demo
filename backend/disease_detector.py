#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
病虫害检测模块
使用深度学习模型识别农作物病虫害
"""

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import joblib
import json
from pathlib import Path

class DiseaseDetector:
    """农作物病虫害检测器"""
    
    def __init__(self, model_path="models/disease_detection_model.h5"):
        """
        初始化病虫害检测器
        
        Args:
            model_path: 训练好的模型文件路径
        """
        self.model_path = model_path
        self.model = None
        self.class_names = [
            '健康', '细菌性叶斑病', '病毒病', '真菌感染',
            '蚜虫', '红蜘蛛', '白粉虱', '蓟马',
            '营养缺乏', '日灼病'
        ]
        
        # 疾病治疗方案数据库
        self.treatment_database = {
            '细菌性叶斑病': {
                'symptoms': '叶片出现水渍状斑点，后期变为褐色或黑色',
                'causes': '细菌感染，通常在高温高湿环境下发生',
                'treatments': [
                    '喷施铜制杀菌剂（硫酸铜、氢氧化铜）',
                    '改善通风条件，降低湿度',
                    '清除病叶，避免交叉感染',
                    '适当减少浇水频率'
                ],
                'prevention': [
                    '合理密植，保证通风',
                    '避免叶面长时间湿润',
                    '定期检查，及早发现',
                    '轮作种植，减少病原菌积累'
                ]
            },
            '病毒病': {
                'symptoms': '叶片变色、畸形、花叶症状',
                'causes': '病毒感染，通过昆虫传播或机械传播',
                'treatments': [
                    '暂无特效药物，以预防为主',
                    '及时清除感病植株',
                    '防治传播媒介昆虫',
                    '加强植株营养管理'
                ],
                'prevention': [
                    '选用抗病品种',
                    '控制蚜虫等传播媒介',
                    '避免机械损伤',
                    '建立隔离带'
                ]
            },
            '蚜虫': {
                'symptoms': '叶片卷曲、变黄，可见小虫聚集',
                'causes': '蚜虫吸食植物汁液',
                'treatments': [
                    '喷施吡虫啉、啶虫脒等杀虫剂',
                    '释放瓢虫等天敌昆虫',
                    '用肥皂水冲洗叶片',
                    '黄色粘虫板诱杀'
                ],
                'prevention': [
                    '定期检查，及早发现',
                    '保护天敌昆虫',
                    '合理施肥，增强抗性',
                    '清除杂草，减少虫源'
                ]
            }
        }
    
    def load_model(self):
        """加载预训练模型"""
        try:
            if Path(self.model_path).exists():
                self.model = load_model(self.model_path)
                print(f"模型加载成功: {self.model_path}")
                return True
            else:
                print(f"模型文件不存在: {self.model_path}")
                return False
        except Exception as e:
            print(f"模型加载失败: {e}")
            return False
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """
        图像预处理
        
        Args:
            image_path: 图片路径
            target_size: 目标尺寸
            
        Returns:
            预处理后的图像数组
        """
        try:
            # 读取图像
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"无法读取图片: {image_path}")
            
            # 转换为RGB格式
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # 调整大小
            image = cv2.resize(image, target_size)
            
            # 转换为数组并归一化
            image = img_to_array(image)
            image = image.astype('float32') / 255.0
            
            # 添加批次维度
            image = np.expand_dims(image, axis=0)
            
            return image
            
        except Exception as e:
            print(f"图像预处理失败: {e}")
            return None
    
    def predict_disease(self, image_path):
        """
        病虫害识别预测
        
        Args:
            image_path: 图片路径
            
        Returns:
            识别结果字典
        """
        # 预处理图像
        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return {'error': '图像预处理失败'}
        
        # 模拟预测结果（实际应该使用训练好的模型）
        if self.model is None:
            # 模拟预测概率
            predictions = np.random.dirichlet(np.ones(len(self.class_names)))
            predicted_class_idx = np.argmax(predictions)
        else:
            # 使用实际模型预测
            predictions = self.model.predict(processed_image)[0]
            predicted_class_idx = np.argmax(predictions)
        
        predicted_class = self.class_names[predicted_class_idx]
        confidence = float(predictions[predicted_class_idx])
        
        # 获取治疗建议
        treatment_info = self.get_treatment_recommendation(predicted_class)
        
        result = {
            'predicted_disease': predicted_class,
            'confidence': confidence,
            'all_predictions': {
                self.class_names[i]: float(predictions[i])
                for i in range(len(self.class_names))
            },
            'treatment': treatment_info,
            'risk_level': self.assess_risk_level(predicted_class, confidence)
        }
        
        return result
    
    def get_treatment_recommendation(self, disease_name):
        """
        获取治疗建议
        
        Args:
            disease_name: 疾病名称
            
        Returns:
            治疗建议字典
        """
        if disease_name == '健康':
            return {
                'status': '植物健康',
                'recommendations': [
                    '继续保持良好的种植管理',
                    '定期检查植物状态',
                    '适当施肥和浇水',
                    '预防病虫害发生'
                ]
            }
        
        if disease_name in self.treatment_database:
            return self.treatment_database[disease_name]
        else:
            return {
                'status': '未知疾病',
                'recommendations': [
                    '建议咨询专业农技人员',
                    '隔离疑似感病植株',
                    '详细记录症状特征',
                    '寻求专业诊断'
                ]
            }
    
    def assess_risk_level(self, disease_name, confidence):
        """
        评估风险等级
        
        Args:
            disease_name: 疾病名称
            confidence: 置信度
            
        Returns:
            风险等级
        """
        if disease_name == '健康':
            return '无风险'
        
        # 高风险疾病
        high_risk_diseases = ['病毒病', '细菌性叶斑病']
        
        if disease_name in high_risk_diseases and confidence > 0.8:
            return '高风险'
        elif confidence > 0.6:
            return '中风险'
        else:
            return '低风险'
    
    def batch_predict(self, image_paths):
        """
        批量预测
        
        Args:
            image_paths: 图片路径列表
            
        Returns:
            预测结果列表
        """
        results = []
        for image_path in image_paths:
            result = self.predict_disease(image_path)
            result['image_path'] = image_path
            results.append(result)
        
        return results
    
    def generate_report(self, results):
        """
        生成诊断报告
        
        Args:
            results: 预测结果列表
            
        Returns:
            格式化的报告
        """
        report = {
            'summary': {
                'total_images': len(results),
                'healthy_count': 0,
                'disease_count': 0,
                'high_risk_count': 0
            },
            'details': results,
            'recommendations': []
        }
        
        # 统计信息
        for result in results:
            if result['predicted_disease'] == '健康':
                report['summary']['healthy_count'] += 1
            else:
                report['summary']['disease_count'] += 1
                
            if result['risk_level'] == '高风险':
                report['summary']['high_risk_count'] += 1
        
        # 生成总体建议
        if report['summary']['high_risk_count'] > 0:
            report['recommendations'].append('发现高风险病虫害，建议立即采取治疗措施')
        
        if report['summary']['disease_count'] > report['summary']['total_images'] * 0.3:
            report['recommendations'].append('病虫害发生率较高，建议加强防控管理')
        
        return report

# 使用示例
if __name__ == "__main__":
    # 初始化检测器
    detector = DiseaseDetector()
    
    # 尝试加载模型
    detector.load_model()
    
    # 模拟单张图片检测
    image_path = "sample_images/plant_leaf.jpg"
    result = detector.predict_disease(image_path)
    
    print("=== 病虫害检测结果 ===")
    print(f"预测疾病: {result['predicted_disease']}")
    print(f"置信度: {result['confidence']:.2%}")
    print(f"风险等级: {result['risk_level']}")
    
    if 'treatment' in result:
        print("\n=== 治疗建议 ===")
        treatment = result['treatment']
        if 'treatments' in treatment:
            for i, treatment_option in enumerate(treatment['treatments'], 1):
                print(f"{i}. {treatment_option}")
    
    # 模拟批量检测
    image_paths = ["sample1.jpg", "sample2.jpg", "sample3.jpg"]
    batch_results = detector.batch_predict(image_paths)
    
    # 生成报告
    report = detector.generate_report(batch_results)
    print(f"\n=== 批量检测报告 ===")
    print(f"检测图片总数: {report['summary']['total_images']}")
    print(f"健康植株: {report['summary']['healthy_count']}")
    print(f"病虫害植株: {report['summary']['disease_count']}")
    print(f"高风险病例: {report['summary']['high_risk_count']}")