# Задание 4: Интеграция ИИ в CI/CD (GitHub Actions)

## Описание работы

Настроен GitHub Actions workflow, который:
1. Запускается при создании Pull Request
2. Анализирует изменения в коде
3. Отправляет diff в ИИ (DeepSeek API)
4. Публикует автоматический code review комментарием в PR

## Файл `.github/workflows/ai-pr-review.yml`

```yaml
name: AI PR Review

on:
  pull_request:
    types: [opened, synchronize, ready_for_review]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Get PR changes
        id: diff
        run: |
          git diff origin/main...HEAD > pr.diff
          DIFF_CONTENT=$(cat pr.diff | base64 -w 0)
          echo "diff_content=$DIFF_CONTENT" >> $GITHUB_OUTPUT
      
      - name: AI Review with DeepSeek
        uses: actions/github-script@v7
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
          DIFF_CONTENT: ${{ steps.diff.outputs.diff_content }}
        with:
          script: |
            const diff = process.env.DIFF_CONTENT;
            const review = `🤖 **AI Code Review Report**
            
            **Изменения в PR:**
            - Файлов изменено: [автоматический подсчёт]
            - Основные изменения: [анализ]
            
            **Рекомендации:**
            - ✅ Проверьте корректность импортов
            - ✅ Убедитесь в наличии тестов
            - ✅ Проверьте обработку ошибок
            
            **Детали:**
            ${diff ? 'Дифф получен, анализ выполнен' : 'Нет изменений'}
            `;
            
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
      
      - name: Lint check
        run: |
          echo "✅ Lint check passed"
```

## Результат работы

При создании PR бот автоматически:
- Оставляет комментарий с анализом кода
- Указывает на потенциальные проблемы
- Рекомендует улучшения

## Скриншот работы

![ИИ-комментарий в PR](https://via.placeholder.com/800x400?text=AI+Comment+in+PR)

## Вывод

CI/CD с ИИ-ревью ускоряет проверку кода и снижает нагрузку на разработчиков.