import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "SODL Language Support" is now active!');

    // Register a simple command to show SODL info
    const disposable = vscode.commands.registerCommand('sodl-language.showInfo', () => {
        vscode.window.showInformationMessage('SODL (Specification Orchestration Definition Language) - A DSL for controlled AI-driven code generation');
    });

    context.subscriptions.push(disposable);
}

export function deactivate() {}
