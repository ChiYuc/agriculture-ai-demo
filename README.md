# 🌱 农业AI智能解决方案

<div align="center">

![Agriculture AI](https://img.shields.io/badge/Agriculture-AI-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-18-cyan)
![Machine Learning](https://img.shields.io/badge/ML-TensorFlow-orange)

一个基于人工智能和机器学习的农业智能决策支持系统

</div>

## 🚀 项目简介

农业AI智能解决方案是一个综合性的Web平台，利用机器学习算法为农民和农业专家提供智能化的农业决策支持。系统集成了多种AI模型，能够：

- 🌾 **作物推荐**: 根据土壤和环境条件推荐最适合的作物
- 🧪 **土壤分析**: 分析土壤质量并提供改良建议  
- 💧 **灌溉优化**: 智能灌溉调度和用水量预测
- 🐛 **病虫害识别**: 通过图像识别诊断作物病虫害
- 📊 **产量预测**: 预测作物产量并提供种植建议

## 🛠️ 技术栈

### 前端
- **React 18** - 现代化用户界面
- **TypeScript** - 类型安全的开发体验
- **Tailwind CSS** - 响应式UI设计
- **Chart.js** - 数据可视化

### 后端
- **Python Flask** - 轻量级Web框架
- **FastAPI** - 高性能API服务
- **PostgreSQL** - 主数据库
- **Redis** - 缓存和会话管理

### AI/ML
- **TensorFlow** - 深度学习模型
- **Scikit-learn** - 传统机器学习算法
- **OpenCV** - 计算机视觉处理
- **Pandas** - 数据处理和分析

## 📋 功能特性

### 1. 智能作物推荐
基于以下参数提供最优作物推荐：
- 土壤pH值、氮磷钾含量
- 气候条件（温度、湿度、降雨量）
- 历史种植数据
- 市场价格趋势

### 2. 土壤健康监测
- 实时土壤质量评估
- 营养成分缺陷检测
- 改良方案推荐
- 施肥计划制定

### 3. 病虫害智能诊断
- 上传作物照片进行AI诊断
- 识别常见病虫害类型
- 提供治疗方案和预防措施
- 用药建议和安全指导

### 4. 产量预测与优化
- 基于历史数据的产量预测
- 种植密度优化建议
- 收获时间预测
- 经济效益分析

## 🔧 安装与运行

### 环境要求
- Node.js >= 16
- Python >= 3.8
- PostgreSQL >= 12
- Redis >= 6

### 快速启动

1. **克隆项目**
```bash
git clone https://github.com/ChiYuc/agriculture-ai-demo.git
cd agriculture-ai-demo
```

2. **安装前端依赖**
```bash
cd frontend
npm install
npm run dev
```

3. **安装后端依赖**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

4. **配置数据库**
```bash
# 创建数据库
createdb agriculture_ai

# 运行迁移
python manage.py db upgrade
```

## 📊 API文档

### 作物推荐API
```http
POST /api/crop-recommendation
Content-Type: application/json

{
  "nitrogen": 90,
  "phosphorus": 42,
  "potassium": 43,
  "temperature": 20.8,
  "humidity": 82,
  "ph": 6.5,
  "rainfall": 202.9
}
```

### 病虫害识别API
```http
POST /api/disease-detection
Content-Type: multipart/form-data

{
  "image": [文件],
  "crop_type": "tomato"
}
```

## 🎯 项目路线图

- [x] 基础框架搭建
- [x] 作物推荐模型开发
- [x] 用户界面设计
- [ ] 病虫害识别模型训练
- [ ] 移动端应用开发
- [ ] 实时数据接入
- [ ] 多语言支持

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 贡献方式
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👥 团队

- **项目负责人**: 农业AI团队
- **技术负责人**: 机器学习工程师
- **产品经理**: 农业专家

## 📞 联系我们

- 📧 Email: contact@agriculture-ai.com
- 🌐 Website: https://agriculture-ai-demo.com
- 💬 Discord: [农业AI社区](https://discord.gg/agriculture-ai)

---

<div align="center">
  <p>⭐ 如果这个项目对您有帮助，请给我们一个star！</p>
  <p>🚀 让我们一起用AI技术推动农业现代化！</p>
</div>