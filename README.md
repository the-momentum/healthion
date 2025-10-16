<div align="center">
  <img src="https://cdn.prod.website-files.com/66a1237564b8afdc9767dd3d/66df7b326efdddf8c1af9dbb_Momentum%20Logo.svg" height="64">

  [![Contact us](https://img.shields.io/badge/Contact%20us-AFF476.svg)](mailto:hello@themomentum.ai?subject=Terraform%20Modules)
  [![Check Momentum](https://img.shields.io/badge/Check%20Momentum-1f6ff9.svg)](https://themomentum.ai)
  [![MIT License](https://img.shields.io/badge/License-MIT-636f5a.svg?longCache=true)](LICENSE)
</div>

# Healthion

Take charge of your wearable data with AI-powered health insights. One central repository for all your wearable data, leveraging cutting-edge AI models (including local ones) to provide personalized health analytics and actionable insights. Transform your fitness trackers into intelligent health companions.

## Motivation 

At Momentum, we've worked on numerous projects that utilized wearable device data. We know that integrations can be challenging. We've developed both completely custom solutions for integrating wearable data and leveraged SaaS platforms that provide such integrations. Based on these experiences, we decided to create something that will be community-driven. We want to enable developers to build AI agents based on wearable data. We want to enable building solutions for both individuals and professionals. 

## Core Features
- 📱 **Easy Data Import**: Connect your favorite fitness trackers and health apps in one place
- 🧠 **Smart Data Processing**: Automatically organize and clean your health data for better insights
- 🤖 **AI-Ready Format**: Your data is prepared for AI analysis, making it easy to get personalized health recommendations
- 💬 **AI Assistant Integration**: Connect with AI tools through MCP Server to ask questions about your health data
- 📊 **Beautiful Dashboard**: View and explore your health data through an intuitive web interface

## Ecosystem

### Backend

**healthion-api** - FastAPI-based REST API that serves as the central data hub for wearable health data. Features comprehensive data models for heart rate, workouts, active energy, and user management. Includes authentication, data import services, and unified endpoints for accessing normalized health metrics. Built with PostgreSQL, SQLAlchemy, and Alembic for robust data persistence and migration management. See [healthion-api/README.md](healthion-api/README.md) for detailed setup and usage instructions. 

### Frontend

**healthion-web** - Modern React-based web application built with Vite, TypeScript, and shadcn/ui components. Features comprehensive health data visualization with dedicated pages for heart rate analytics, workout tracking, and data import functionality. Includes Auth0 authentication, responsive design, and seamless API integration with the backend. Built with Tailwind CSS for styling and React Router for navigation. See [healthion-web/README.md](healthion-web/README.md) for detailed setup and usage instructions. 


### MCP Server

**healthion-mcp** - Model Context Protocol (MCP) server that provides AI assistants with access to health and fitness data tools. Built with FastMCP, it serves as a bridge between AI agents and the Healthion health data ecosystem. Features modular architecture with dedicated tools for heart rate data, workouts, and fitness metrics. Enables AI assistants to query and interact with user health data through standardized MCP protocol with HTTP transport optimization for AI agent integrations. See [healthion-mcp/README.md](healthion-mcp/README.md) for detailed setup and usage instructions.


## Getting Started

To get started with Healthion, each component needs to be set up independently. Please refer to the individual README files for detailed setup instructions:

- **Backend API**: See [healthion-api/README.md](healthion-api/README.md) for API setup and configuration
- **Frontend Web App**: See [healthion-web/README.md](healthion-web/README.md) for web application setup
- **MCP Server**: See [healthion-mcp/README.md](healthion-mcp/README.md) for MCP server configuration

**Future Plans**: We're working on a unified Docker setup that will run all components together with a single command, making the initial setup much simpler. Stay tuned for updates! 🐳


## Roadmap 

We're just getting started, but the vision is ambitious! We're currently working on:

**🔌 Wearable Integrations**
- [ ] **Garmin Support**: Full integration with Garmin Connect API
- [ ] **Oura Ring**: Sleep and recovery data synchronization
- [ ] **WHOOP**: Advanced fitness and recovery metrics

**📊 Data Processing**
- [ ] **Smart Normalization**: Automatic data standardization across different devices
- [ ] **Deduplication Engine**: Remove duplicate entries from multiple sources
- [ ] **Data Quality Scoring**: Assess and improve data reliability

**🤖 AI & Analytics**
- [ ] **Pre-built AI Insights**: Local and cloud-based health insights
- [ ] **Predictive Analytics**: Trend analysis and health predictions
- [ ] **Personalized Recommendations**: AI-driven health suggestions
- [ ] **Anomaly Detection**: Identify unusual patterns in health data

**📚 Documentation & Examples**
- [ ] **Comprehensive Documentation**: Detailed guides and API references
- [ ] **Use Case Examples**: Real-world implementation scenarios
- [ ] **Tutorial Series**: Step-by-step guides for developers
- [ ] **Community Showcase**: Featured projects and integrations

**🚀 Platform Features**
- [ ] **Unified Docker Setup**: One-command deployment for all components
- [ ] **Advanced Dashboard**: Enhanced data visualization and analytics
- [ ] **Mobile App**: Native mobile experience for health data
- [ ] **API Rate Limiting**: Production-ready API management 

## Contribute

🚀 **Join the Future of Health Data & AI!** 

The world of wearables and AI is evolving at breakneck speed. New devices hit the market monthly, AI models become more powerful by the day, and the possibilities for personalized health insights are expanding exponentially. 

**We're looking for contributors who are passionate about:**
- 🔌 **Wearable Integrations**: Help us support the latest fitness trackers and health devices
- 🤖 **AI & ML**: Improve data processing, normalization, and AI-ready data formats
- 🎨 **User Experience**: Make health data more accessible and beautiful
- 📚 **Documentation**: Help others understand and use our platform
- 🧪 **Testing**: Ensure reliability across different devices and scenarios

**Every contribution matters** - from fixing bugs to adding new wearable support, from improving documentation to suggesting new features. The wearable and AI landscape changes rapidly, and your input helps us stay ahead of the curve.

Need help? Looking for guidance on use cases or implementation? Don't hesitate to ask your question in our [GitHub discussion forum](https://github.com/the-momentum/healthion/discussions)! You'll also find interesting use cases, tips, and community insights there.



