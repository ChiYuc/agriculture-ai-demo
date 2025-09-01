import React, { useState } from 'react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('crop');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [formData, setFormData] = useState({
    nitrogen: '',
    phosphorus: '',
    potassium: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: ''
  });

  const tabs = [
    { id: 'crop', name: '作物推荐', icon: '🌾' },
    { id: 'soil', name: '土壤分析', icon: '🪨' },
    { id: 'weather', name: '天气预报', icon: '🌤️' },
    { id: 'disease', name: '病虫害检测', icon: '🐛' }
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const submitCropRecommendation = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/crop-recommendation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('API调用失败:', error);
      setResult({ error: '网络连接失败，请检查后端服务是否启动' });
    }
    setLoading(false);
  };

  const renderCropRecommendation = () => (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-6 text-green-600">🌾 智能作物推荐</h2>
      
      <div className="grid grid-cols-2 gap-6 mb-6">
        <div>
          <label className="block text-sm font-medium mb-2">氮含量 (N)</label>
          <input
            type="number"
            name="nitrogen"
            value={formData.nitrogen}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            placeholder="mg/kg"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">磷含量 (P)</label>
          <input
            type="number"
            name="phosphorus"
            value={formData.phosphorus}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            placeholder="mg/kg"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">钾含量 (K)</label>
          <input
            type="number"
            name="potassium"
            value={formData.potassium}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            placeholder="mg/kg"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">温度 (°C)</label>
          <input
            type="number"
            name="temperature"
            value={formData.temperature}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            placeholder="摄氏度"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">湿度 (%)</label>
          <input
            type="number"
            name="humidity"
            value={formData.humidity}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            placeholder="百分比"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">pH值</label>
          <input
            type="number"
            step="0.1"
            name="ph"
            value={formData.ph}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            placeholder="0-14"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-2">降雨量 (mm)</label>
          <input
            type="number"
            name="rainfall"
            value={formData.rainfall}
            onChange={handleInputChange}
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
            placeholder="毫米"
          />
        </div>
      </div>
      
      <button
        onClick={submitCropRecommendation}
        disabled={loading}
        className="w-full bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-lg transition-colors duration-200 disabled:opacity-50"
      >
        {loading ? '分析中...' : '🔍 获取作物推荐'}
      </button>
      
      {result && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          {result.error ? (
            <div className="text-red-600">
              <h3 className="font-bold">❌ 错误</h3>
              <p>{result.error}</p>
            </div>
          ) : (
            <div>
              <h3 className="font-bold text-lg mb-2">📊 推荐结果</h3>
              <div className="bg-green-100 p-4 rounded-lg mb-4">
                <p className="text-lg">
                  <span className="font-bold">推荐作物：</span>
                  <span className="text-green-600 text-xl">{result.recommended_crop}</span>
                </p>
                <p className="text-sm text-gray-600">
                  置信度: {(result.confidence * 100).toFixed(1)}%
                </p>
              </div>
              
              {result.suggestions && result.suggestions.length > 0 && (
                <div>
                  <h4 className="font-bold mb-2">💡 种植建议</h4>
                  <ul className="list-disc list-inside space-y-1">
                    {result.suggestions.map((suggestion, index) => (
                      <li key={index} className="text-sm">{suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );

  const renderActiveComponent = () => {
    switch (activeTab) {
      case 'crop':
        return renderCropRecommendation();
      case 'soil':
        return <div className="p-8 text-center">🪨 土壤分析功能开发中...</div>;
      case 'weather':
        return <div className="p-8 text-center">🌤️ 天气预报功能开发中...</div>;
      case 'disease':
        return <div className="p-8 text-center">🐛 病虫害检测功能开发中...</div>;
      default:
        return renderCropRecommendation();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      {/* 导航栏 */}
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🌱</span>
              <h1 className="text-2xl font-bold text-green-600">
                农业AI智能决策系统
              </h1>
            </div>
            <div className="flex space-x-1">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-4 py-2 rounded-lg flex items-center space-x-2 transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-green-500 text-white shadow-md'
                      : 'text-gray-600 hover:bg-green-100'
                  }`}
                >
                  <span>{tab.icon}</span>
                  <span>{tab.name}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* 主要内容区域 */}
      <main className="max-w-7xl mx-auto py-8 px-4">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {renderActiveComponent()}
        </div>
      </main>

      {/* 页脚 */}
      <footer className="bg-gray-800 text-white py-8 mt-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-lg mb-2">🌱 农业AI智能决策系统</p>
          <p className="text-gray-400">
            利用人工智能技术，为现代农业提供智能化解决方案
          </p>
          <div className="mt-4 flex justify-center space-x-6">
            <a href="#" className="text-gray-400 hover:text-white">
              📧 联系我们
            </a>
            <a href="#" className="text-gray-400 hover:text-white">
              📖 使用指南
            </a>
            <a href="#" className="text-gray-400 hover:text-white">
              🔧 API文档
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;