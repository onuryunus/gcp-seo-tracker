# Install dependencies using uv package manager
install:
	@command -v uv >/dev/null 2>&1 || { echo "uv is not installed. Installing uv..."; curl -LsSf https://astral.sh/uv/0.6.12/install.sh | sh; source $HOME/.local/bin/env; }
	uv sync --dev
# Launch local dev playground
playground:
	@echo "==============================================================================="
	@echo "| 🚀 Starting your agent playground...                                        |"
	@echo "|                                                                             |"
	@echo "| 💡 Try asking: What's the weather in San Francisco?                         |"
	@echo "|                                                                             |"
	@echo "| 🔍 IMPORTANT: Select the 'app' folder to interact with your agent.          |"
	@echo "==============================================================================="
	uv run adk web . --port 8501 --reload_agents

# Deploy the agent remotely
backend:
	# Export dependencies to requirements file using uv export.
	uv export --no-hashes --no-header --no-dev --no-emit-project --no-annotate > .requirements.txt 2>/dev/null || \
	uv export --no-hashes --no-header --no-dev --no-emit-project > .requirements.txt && uv run app/agent_engine_app.py

# Install client dependencies
install-client:
	cd client && npm install --legacy-peer-deps

# Start the custom FastAPI server
server:
	@echo "==============================================================================="
	@echo "| 🚀 Starting PubTender API Server...                                         |"
	@echo "|                                                                             |"
	@echo "| 🌐 Server will be available at: http://localhost:8000                       |"
	@echo "| 📡 WebSocket endpoint: ws://localhost:8000/ws/{user_id}                     |"
	@echo "==============================================================================="
	cd server && python3 main.py

# Start the React client
client:
	@echo "==============================================================================="
	@echo "| 🚀 Starting PubTender Client...                                             |"
	@echo "|                                                                             |"
	@echo "| 🌐 Client will be available at: http://localhost:3000                       |"
	@echo "==============================================================================="
	cd client && npm run dev

# Start both client and server in parallel
dev:
	@echo "==============================================================================="
	@echo "| 🚀 Starting PubTender Full Stack Application...                             |"
	@echo "|                                                                             |"
	@echo "| 🖥️  Frontend: http://localhost:3000                                          |"
	@echo "| 🔧 Backend:  http://localhost:8000                                          |"
	@echo "==============================================================================="
	@make -j2 server client

# Set up development environment resources using Terraform
setup-dev-env:
	PROJECT_ID=$$(gcloud config get-value project) && \
	(cd deployment/terraform/dev && terraform init && terraform apply --var-file vars/env.tfvars --var dev_project_id=$$PROJECT_ID --auto-approve)

# Run unit and integration tests
test:
	uv run pytest tests/unit && uv run pytest tests/integration

# Run code quality checks (codespell, ruff, mypy)
lint:
	uv sync --dev --extra lint
	uv run codespell
	uv run ruff check . --diff
	uv run ruff format . --check --diff
	uv run mypy .