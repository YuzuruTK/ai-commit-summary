import os
import requests
import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv(".env")

# --- Configuration ---
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
AI_API_KEY = os.getenv("AI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DAYS = 30  # commits from the last 7 days
client = Groq(api_key=AI_API_KEY)

# --- GitHub Commit Search ---
since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=DAYS)).date().isoformat()
url = f"https://api.github.com/search/commits?q=author:{GITHUB_USERNAME}+committer-date:>{since}"
headers = {
    "Accept": "application/vnd.github.cloak-preview+json",  # needed for commit search
    "Authorization": f"token {GITHUB_TOKEN}"
}


response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"Error {response.status_code}: {response.text}")
    exit()

data = response.json()

if not data.get("items"):
    print(f"No commits found in the last {DAYS} days.")
# else:
#     for commit in data["items"]:
#         repo = commit["repository"]["full_name"]
#         message = commit["commit"]["message"].split("\n")[0]
#         date = commit["commit"]["author"]["date"]
#         print(f"[{repo}] {date}\n→ {message}\n")

print(f"Total commits found: {len(data.get('items', []))}")

# --- AI Summary ---
ai_model = "openai/gpt-oss-120b"
content = f"""create a LinkedIn post in Portuguese based on the following commit message made by the user {GITHUB_USERNAME} in the last 30 days. The post must be in a good format for LinkedIn, like this template and remember to NOT create information out of the commit messages:

Nesta semana, foquei em [resumo do foco principal da semana — ex: otimização de performance, reestruturação da arquitetura, integração com API, etc.].

💻 Avanços técnicos

Implementação de [feature principal — ex: autenticação JWT, sistema de cache, pipeline de dados].

Refatoração de [componente / módulo] para [motivo técnico — ex: melhorar legibilidade, reduzir acoplamento].

Testes de [tecnologia / serviço] para [objetivo — ex: medir performance, validar compatibilidade].

Correção de [bug / gargalo] que afetava [comportamento / desempenho].

📚 Tecnologias e conceitos aplicados

[Linguagem / framework / lib] para [função — ex: requisições assíncronas, renderização dinâmica, serialização].

[Ferramenta / serviço cloud] para [ex: armazenamento, deploy, automação].

[Padrão de projeto / princípio de engenharia] aplicado em [parte do sistema].

🧠 Aprendizados da semana

[Insight técnico — ex: a importância de configurar índices antes de otimizar queries].

[Boa prática / conceito — ex: o impacto de desacoplar lógica de negócio dos endpoints].

[Reflexão curta — ex: pequenas mudanças de arquitetura podem ter efeitos enormes em escalabilidade].

📈 Próximos passos

[Objetivo da próxima semana — ex: iniciar testes de carga, implementar CI/CD, integrar com API externa].

(Opcional) 🤝 Conclusão / Engajamento leve
Se alguém já trabalhou com [tecnologia / desafio similar], gostaria de saber como abordaram [problema específico].

#softwaredevelopment #backend #cloud #datapipeline #progressupdate

Here is the commit message:\n
""" + "\n".join([f"{commit['repository']['full_name']} - {commit['commit']['message']}" for commit in data.get("items", [])])

completion = client.chat.completions.create(
    model=ai_model,
    messages=[
      {
        "role": "user",
        "content": content
      },
    ],
    temperature=1,
    max_completion_tokens=8192,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None 
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")