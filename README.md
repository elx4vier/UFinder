````markdown
# 🔍 UFinder for Ulauncher

**UFinder** é uma extensão de busca de arquivos ultra-rápida para o Ulauncher. Ela indexa sua pasta Home em segundo plano, permitindo que você encontre documentos, imagens, pastas e arquivos de sistema instantaneamente, sem travar a interface.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Ulauncher](https://img.shields.io/badge/Ulauncher-v5.0+-orange)

---

## ✨ Funcionalidades

- ⚡ **Busca em tempo real:** Indexação inteligente que não consome sua CPU  
- 📂 **Reconhecimento de Pastas do Sistema:** Ícones e descrições personalizadas para Desktop, Downloads, Documentos, etc.  
- 🌍 **Internacionalização (i18n):** Suporte automático para Português, Inglês, Espanhol, Alemão, Francês e Russo  
- 🖼️ **Preview de Ícones:** Ícones específicos para PDFs, Imagens, Músicas, Vídeos e Planilhas  
- ⚙️ **Ações Customizáveis:** Escolha entre abrir o arquivo diretamente ou revelar a pasta no seu gerenciador de arquivos  

---

## 🚀 Instalação

1. Abra as preferências do Ulauncher  
2. Vá em **Extensions → Add extension**  
3. Cole a URL do repositório:

```text
https://github.com/seu-usuario/ufinder
````

---

## 🛠️ Configuração

Após instalar, você pode ajustar as preferências:

| Opção              | Descrição                                                     | Padrão |
| ------------------ | ------------------------------------------------------------- | ------ |
| **Keyword**        | Atalho para ativar a busca                                    | `f`    |
| **Results limit**  | Quantidade de itens exibidos                                  | `9`    |
| **Default action** | `Open` (abre o arquivo) ou `Reveal` (abre a pasta do arquivo) | `Open` |

---

## 📁 Estrutura de Tradução

A extensão detecta automaticamente o idioma do sistema. Para adicionar um novo idioma, crie um arquivo `.json` na pasta `/translations`:

```text
translations/
├── en.json (default)
├── pt.json
├── es.json
├── fr.json
├── de.json
└── ru.json
```

---

## 📝 Licença

Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais informações.

---

## 👨‍💻 Autor

Desenvolvido por **Xavier**

```
