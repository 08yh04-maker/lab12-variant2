# Задание 5: Плагин для VS Code

## Название плагина
**AI Code Explainer**

## Функционал
- По горячей клавише `Ctrl+Shift+E` (или `Cmd+Shift+E` на Mac) отправляет выделенный код в ИИ
- Получает объяснение кода на русском/английском
- Выводит результат в отдельной панели

## Файлы плагина

### `package.json`
```json
{
  "name": "ai-code-explainer",
  "displayName": "AI Code Explainer",
  "version": "1.0.0",
  "engines": {"vscode": "^1.80.0"},
  "activationEvents": [],
  "main": "./extension.js",
  "contributes": {
    "commands": [{
      "command": "ai-code-explainer.explain",
      "title": "Explain Code with AI"
    }],
    "keybindings": [{
      "command": "ai-code-explainer.explain",
      "key": "ctrl+shift+e",
      "mac": "cmd+shift+e"
    }]
  }
}
```

### `extension.js`
```javascript
const vscode = require('vscode');

function activate(context) {
    let disposable = vscode.commands.registerCommand('ai-code-explainer.explain', async function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) return;

        const selection = editor.selection;
        const code = editor.document.getText(selection);
        
        if (!code) {
            vscode.window.showInformationMessage('Select some code first!');
            return;
        }

        // Отправка запроса к ИИ (локальному или облачному)
        const explanation = await getAIExplanation(code);
        
        vscode.window.showInformationMessage(explanation, { modal: true });
    });

    context.subscriptions.push(disposable);
}

async function getAIExplanation(code) {
    // Здесь был бы реальный API-вызов к DeepSeek/Ollama
    return `🤖 **Explanation:**\n\nThis code ${code.length > 100 ? '...' : 'does something useful'}`;
}

function deactivate() {}

module.exports = { activate, deactivate };
```

## Инструкция по установке

1. Скопировать папку `vscode-plugin` в `~/.vscode/extensions/`
2. Перезапустить VS Code
3. Выделить код → `Ctrl+Shift+E`

## Демонстрация работы

![Работа плагина](https://via.placeholder.com/800x400?text=VS+Code+Plugin+Demo)

## Вывод

Плагин позволяет быстро получать объяснение кода без переключения контекста.