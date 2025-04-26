.PHONY: install
install: ## 安装虚拟环境和依赖
	@echo "🚀 创建虚拟环境并安装依赖"
	@uv sync
	@uv run pre-commit install

.PHONY: check
check: ## 运行代码质量检查工具
	@echo "🚀 检查 lock 文件与 pyproject.toml 的一致性"
	@uv lock --locked
	@echo "🚀 运行代码检查: pre-commit"
	@uv run pre-commit run -a
	# @echo "🚀 运行类型检查"
	# @uv run mypy
	# @echo "🚀 检查过时依赖"
	# @uv run deptry .
	@echo "🚀 检查完成"

.PHONY: dev
dev: ## 运行开发服务器
	@echo "🚀 启动停车场MCP服务"
	@uv run python main.py

.PHONY: test
test: ## 运行测试
	@echo "🚀 运行测试: pytest"
	@uv run python -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## 构建项目
	@echo "🚀 创建 wheel 文件"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## 清理构建 artifacts
	@echo "🚀 清理构建 artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
