#!/bin/bash

echo "🚀 Bhrahma GitHub Deployment Script"
echo "===================================="
echo ""
echo "Pushing code to GitHub..."
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Code deployed to GitHub!"
    echo "📍 Repository: https://github.com/iamrajp/Bhrahma"
    echo ""
else
    echo "❌ Push failed."
    echo "If the repository doesn't exist, create it at:"
    echo "https://github.com/new?name=Bhrahma&description=Advanced+AI+agentic+system+with+skill+learning+capabilities+-+Multi-LLM+support%2C+Agent+Skills%2C+and+intelligent+task+orchestration&visibility=public"
    echo ""
fi
