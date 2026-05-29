let currentVersion = 'v1';

	    // 显示/隐藏版本菜单
	    function toggleVersionMenu() {
	        const options = document.getElementById('versionOptions');
	        options.style.display = options.style.display === 'block' ? 'none' : 'block';
	    }

	     // 版本切换逻辑
	        function switchVersion(version) {
	            const body = document.body;
	            const currentVerElement = document.getElementById('currentVersion');
	            const loading = document.getElementById('versionLoading');
	            const toast = document.getElementById('versionToast');

	            // 显示加载特效
	            // loading.classList.add('active');

	            // 移除所有版本样式
	            body.classList.remove('v1-theme', 'v2-theme', 'v3-theme');

	            // 应用新版本样式
	            if (version !== 'v1') {
	                body.classList.add(`${version}-theme`);
	            }

	            // 更新显示文本
	            currentVerElement.textContent = version.toUpperCase();
	            currentVersion = version;

	            // 模拟版本切换的延迟
	            setTimeout(() => {
	                // 隐藏加载特效
	                loading.classList.remove('active');

	                // 显示版本切换提示
	                toast.classList.add('active');

	                // 模拟提示的显示时间
	                setTimeout(() => {
	                    toast.classList.remove('active');
	                }, 2000);
	            }, 500);

	            // 关闭菜单
	            document.getElementById('versionOptions').style.display = 'none';

	            // 保存用户偏好
	            localStorage.setItem('ui-version', version);
	        }

	        // 初始化版本
	        window.onload = function() {
	            const savedVersion = localStorage.getItem('ui-version') || 'v1';
	            switchVersion(savedVersion);
	        };

	    // 版本特定布局调整
	    function applyVersionLayout(version) {
	        const container = document.querySelector('.container');
	        switch(version) {
	            case 'v2.0':
	                container.style.maxWidth = '1400px';
	                container.style.padding = '40px';
	                break;
	            case 'v3.0':
	                container.style.maxWidth = '100%';
	                container.style.borderRadius = '0';
	                break;
	            default:
	                container.style.maxWidth = '1200px';
	                container.style.padding = '30px';
	        }
	    }

	    // 初始化版本
	    window.onload = function() {
	        const savedVersion = localStorage.getItem('ui-version') || 'v1';
	        // switchVersion(savedVersion);

	        // 点击页面任意位置关闭菜单
	        document.addEventListener('click', () => {
	            document.getElementById('versionOptions').style.display = 'none';
	        });
	    }
	    let currentType = 'text';

	    function switchInputType(type) {
            clearResult();
	        currentType = type;
	        document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
	        event.target.classList.add('active');

	        const inputArea = document.getElementById('inputArea');
	        inputArea.placeholder = type === 'text' ? '请输入文本内容...' : type === 'file' ? '请上传文档...' : '请输入链接地址...';
	    }

// 高亮显示文本
function highlightText(data) {
    const scrollableTextContainer = document.getElementById('scrollableTextContainer');
    scrollableTextContainer.innerHTML = ''; // 清空容器

    if (data && data.length > 0) {
        data.forEach(item => {
            const p = document.createElement('p');
            p.textContent = item.content;

            // 根据概率设置样式
            if (item.probability >= 0 && item.probability < 50) {
                p.classList.add('green');
            } else if (item.probability >= 50 && item.probability < 70) {
                p.classList.add('yellow');
            } else if (item.probability >= 70 && item.probability < 90) {
                p.classList.add('orange');
            } else if (item.probability >= 90 && item.probability <= 100) {
                p.classList.add('red');
            }

            p.dataset.probability = `虚假概率: ${item.probability}%`;
            scrollableTextContainer.appendChild(p);
        });
    } else {
        scrollableTextContainer.innerHTML = '<p>没有高亮文本可显示。</p>';
    }
}

	    // 新增全局变量记录文件内容
	let currentFileContent = null;
	let currentFileName = null;

	// 修改检测函数
	        function validateInput() {
				// 缩小 left-a
				const leftPanel = document.querySelector('.left-a');
				leftPanel.classList.add('shrink');

				   // 显示 right-panel
				const rightPanel = document.querySelector('.right-a');
				console.log(rightPanel); // 确保 rightPanel 正确获取到元素
				rightPanel.classList.add('show');


	            const inputArea = document.getElementById('inputArea').value.trim();
	            const fileInput = document.getElementById('fileInput').files[0];

	            // 格式校验
	            /*if ((currentType === 'text' && !inputArea) ||
	                (currentType === 'file' && !fileInput) ||
	                (currentType === 'link' && !isValidUrl(inputArea))) {
	                alert(`请输入有效的${currentType === 'text' ? '文本' : currentType === 'file' ? '文件' : '链接'}`);
	                return;
	            }*/

	            // 构造请求数据
	            let requestData = {};
	            if (currentType === 'text') {
	                requestData = { text: inputArea };
                     // 判断文本长度，如果小于150字，不显示 right-a 和高亮文本分析
                if (inputArea.length < 150) {
                     sendRequest(requestData);
                     // 不缩小左侧
            const leftPanel = document.querySelector('.left-a');
            leftPanel.classList.remove('shrink');
                    // 不显示 right-a
                    const rightPanel = document.querySelector('.right-a');
                    rightPanel.classList.remove('show');
                    } else {
                     // 缩小左侧
            const leftPanel = document.querySelector('.left-a');
            leftPanel.classList.add('shrink');
                    // 显示 right-panel
                    const rightPanel = document.querySelector('.right-a');
                     rightPanel.classList.add('show');
                     sendRequest(requestData);
        }
	            } else if (currentType === 'file') {

                    const file = fileInput.files[0];

                    // 创建FormData对象
                    const formData = new FormData();
                    formData.append('file', file); // 'file'是后端接收的参数名

                    // 显示加载状态
                    // document.getElementById('loading').style.display = 'block';
                    if (currentVersion === 'v1'){
                        fetch('http://127.0.0.1:8000/analyzer/bert_file_analyze/', {
                            method: 'POST',
                            body: formData, // 不需要设置Content-Type头部，浏览器会自动设置
                            // 注意：不要手动设置Content-Type，否则multipart边界会出错
                        })
                        .then(response => response.json())
                        .then(data => {
                highlightText(data);
            })
            .catch(error => {
                console.error('上传失败:', error);
                alert("文件上传失败");
            })
            .finally(() => {
                document.getElementById('loading').style.display = 'none';
            });
                    }
                    else if (currentVersion === 'v2.0'){
                        fetch('http://127.0.0.1:8000/analyzer/roberta_file_analyze/', {
                            method: 'POST',
                            body: formData, // 不需要设置Content-Type头部，浏览器会自动设置
                            // 注意：不要手动设置Content-Type，否则multipart边界会出错
                        })
                        .then(response => response.json())
                        .then(data => {
                highlightText(data);
            })
            .catch(error => {
                console.error('上传失败:', error);
                alert("文件上传失败");
            })
            .finally(() => {
                document.getElementById('loading').style.display = 'none';
            });

                    }
                } else if (currentType === 'link') {
	                requestData = { url: inputArea };
	                sendRequest(requestData);
	            }
	        }// 页面加载时设置检测按钮的初始状态
window.onload = function() {
    const detectButton = document.querySelector('.detect');
    detectButton.disabled = true;
};
	// 获取输入框元素
const inputArea = document.getElementById('inputArea');

// 添加输入事件监听器
inputArea.addEventListener('input', function() {
    // 在这里可以添加检测逻辑，例如自动检测或更新按钮状态
    // 例如，如果输入内容超过一定长度，启用检测按钮
    const detectButton = document.querySelector('.detect');
    detectButton.disabled = inputArea.value.trim().length <= 0;
});
	        // 发送请求到后端
	        function sendRequest(requestData) {

                if (currentVersion === 'v1'  && currentType === 'link'){
                    fetch('http://127.0.0.1:8000/analyzer/bert_link_analyze/', {
	                method: 'POST',
	                headers: { 'Content-Type': 'application/json' },
	                body: JSON.stringify(requestData)
	                })
	                .then(response => response.json())
	                .then(data => {
	                // 更新结果展示（保持原有逻辑）
	                updateResults(data);
                      // 显示高亮文本
        highlightText(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('检测失败，请重试！');
    })
    .finally(() => {
        document.getElementById('loading').style.display = 'none';
        document.querySelector('.blur-background').style.display = 'none';
    });


                }
                else if (currentVersion === 'v2.0'  && currentType === 'link'){
                    fetch('http://127.0.0.1:8000/analyzer/roberta_link_analyze/', {
	                method: 'POST',
	                headers: { 'Content-Type': 'application/json' },
	                body: JSON.stringify(requestData)
	                })
	                .then(response => response.json())
	                .then(data => {
                        // 更新结果展示（保持原有逻辑）
                        updateResults(data);
                         // 显示高亮文本
        highlightText(data);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('检测失败，请重试！');
    })
    .finally(() => {
        document.getElementById('loading').style.display = 'none';
        document.querySelector('.blur-background').style.display = 'none';
    });

                }
	            else if (currentVersion === 'v1'  && currentType === 'text'){
                    fetch('http://127.0.0.1:8000/analyzer/bert_content_analyze/', {
	                method: 'POST',
	                headers: { 'Content-Type': 'application/json' },
	                body: JSON.stringify(requestData)
	                })
	                .then(response => response.json())
	                .then(data => {
                        console.log('后端返回的数据:', data); // 调试：打印后端返回的数据
	                // 更新结果展示（保持原有逻辑）
	                updateResults(data);
                    // 如果输入文本超过150字，显示高亮文本
                    if (requestData.text && requestData.text.length > 150) {
                        highlightText(data);
                    } else {
                        // 清空高亮文本容器
                        document.getElementById('highlightedTextContainer').innerHTML = '<h2>高亮文本分析</h2>';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('检测失败，请重试！');
                     })
                    .finally(() => {
                        document.getElementById('loading').style.display = 'none';
                        document.querySelector('.blur-background').style.display = 'none';
                     });
	                // 高光显示文本
					/*
	                highlightText(data);
	                })
	                .catch(error => {
	                console.error('Error:', error);
	                alert('检测失败，请重试！');
	                })
	                .finally(() => {
	                document.getElementById('loading').style.display = 'none';
	                document.querySelector('.blur-background').style.display = 'none';
	                });*/

                }
                else if (currentVersion === 'v2.0'  && currentType === 'text'){
                    fetch('http://127.0.0.1:8000/analyzer/roberta_content_analyze/', {
	                method: 'POST',
	                headers: { 'Content-Type': 'application/json' },
	                body: JSON.stringify(requestData)
	                })
	                .then(response => response.json())
	                .then(data => {
	                // 更新结果展示（保持原有逻辑）
	                updateResults(data);
                    // 如果输入文本超过150字，显示高亮文本
                    if (requestData.text && requestData.text.length > 150) {
                        highlightText(data);
                    } else {
                        // 清空高亮文本容器
                        document.getElementById('highlightedTextContainer').innerHTML = '<h2>高亮文本分析</h2>';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('检测失败，请重试！');
                     })
                    .finally(() => {
                        document.getElementById('loading').style.display = 'none';
                        document.querySelector('.blur-background').style.display = 'none';
                     });
                }
	        }



	        // 提取结果更新逻辑
	        function updateResults(data) {
                 let aiProbability = 0;
        let totalWeight = 0;

        // 如果是段落检测结果，计算加权平均概率
        if (Array.isArray(data) && data.length > 0) {
            for (let item of data) {
                const weight = item.content.length; // 以段落长度为权重
                aiProbability += item.probability * weight;
                totalWeight += weight;
            }
            aiProbability = totalWeight > 0 ? (aiProbability / totalWeight) : 0;
        } else {
            aiProbability = data.probability || 0;
        }

        document.getElementById('aiProbability').textContent = aiProbability.toFixed(2) + '%';
        document.getElementById('progressBar').style.width = aiProbability.toFixed(2) + '%';

	            // 其他指标更新...
	            document.getElementById('textLength').textContent = data.textLength || '0';
	            document.getElementById('vocabularyDiversity').textContent = data.vocabularyDiversity || '0';
	            document.getElementById('sentenceComplexity').textContent = data.sentenceComplexity || '0';
	            document.getElementById('logicalCoherence').textContent = data.logicalCoherence || '0';
	        }


	        // 处理文件输入
	        function handleFileInput() {
	            if (currentType === 'file') {
	                document.getElementById('fileInput').click();
	            }
	        }

	        // 监听文件选择事件
	        document.getElementById('fileInput').addEventListener('change', function(e) {
	            const file = e.target.files[0];
	            if (file) {
	                document.getElementById('inputArea').value = `已选择文件：${file.name}`;
	                document.getElementById('fileDisplay').textContent = `已选择文件：${file.name}`;
	            }
	        });




		function clearResult() {
    // 恢复 left-a 板块的宽度
    const leftPanel = document.querySelector('.left-a');
    leftPanel.classList.remove('shrink');

    // 隐藏 right-a 板块
    const rightPanel = document.querySelector('.right-a');
    rightPanel.classList.remove('show');

    // 清空输入框
    document.getElementById('inputArea').value = '';

    // 清空文件输入
    document.getElementById('fileInput').value = '';

    // 清空文件显示区域
    document.getElementById('fileDisplay').textContent = '';

    // 重置检测结果
    document.getElementById('aiProbability').textContent = '0%';
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('resultText').textContent = '检测结果仅供参考，AI检测技术仍在不断进步中。';

    // 重置分析数据
    document.getElementById('textLength').textContent = '0';
    document.getElementById('vocabularyDiversity').textContent = '0';
    document.getElementById('sentenceComplexity').textContent = '0';
    document.getElementById('logicalCoherence').textContent = '0';

    // 清空链接内容
    document.getElementById('linkContent').innerHTML = '<h2>链接内容</h2>';

    // 清空高亮文本容器
    /*document.getElementById('highlightedTextContainer').innerHTML = '';

    // 隐藏加载动画
    document.getElementById('loading').style.display = 'none';
    document.querySelector('.blur-background').style.display = 'none';*/

    // 重置当前检测类型
    currentType = 'text';
    document.querySelectorAll('.menu-btn').forEach(btn => {btn.classList.remove('active');});
    document.querySelector('.menu-btn:first-child').classList.add('active');

    // 重置输入框占位符
    document.getElementById('inputArea').placeholder = '请输入文本内容...';
}