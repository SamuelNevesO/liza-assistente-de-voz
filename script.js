// Funções de Acessibilidade
function toggleContrast() {
  document.body.classList.toggle('high-contrast');
}

let currentFontSize = 16;
function changeFontSize(step) {
  currentFontSize = Math.min(24, Math.max(14, currentFontSize + step));
  document.documentElement.style.setProperty('--font-size-base', currentFontSize + 'px');
}

// Prepara carregamento de vozes neurais
let vozesDisponiveis = [];
if ('speechSynthesis' in window) {
  window.speechSynthesis.onvoiceschanged = () => {
    vozesDisponiveis = window.speechSynthesis.getVoices();
  };
}

// Simulador de Voz (Web Speech API com Vozes Humanizadas)
function speakText(text) {
  if (!('speechSynthesis' in window)) return;

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'pt-BR';
  utterance.rate = 1.05; // Ritmo mais natural
  utterance.pitch = 1.0;

  if (vozesDisponiveis.length === 0) {
    vozesDisponiveis = window.speechSynthesis.getVoices();
  }

  const vozesPT = vozesDisponiveis.filter(v => v.lang.includes('pt-BR') || v.lang.includes('pt_BR') || v.lang.includes('pt'));

  // Prioriza vozes neurais e de alta qualidade (Edge/Chrome/Apple)
  const melhovoz =
    vozesPT.find(v => v.name.includes('Natural') || v.name.includes('Francisca') || v.name.includes('Thalita')) ||
    vozesPT.find(v => v.name.includes('Google')) ||
    vozesPT.find(v => v.name.includes('Luciana')) ||
    vozesPT[0];

  if (melhovoz) {
    utterance.voice = melhovoz;
  }

  window.speechSynthesis.speak(utterance);
}

function startVoiceDemo() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const statusText = document.getElementById('statusText');
  const userSpeech = document.getElementById('userSpeech');
  const lizaReply = document.getElementById('lizaReply');
  const micBtn = document.getElementById('micBtn');

  if (!SpeechRecognition) {
    const fallbackMsg = "Olá! Sou a Liza, sua assistente virtual de código aberto.";
    userSpeech.innerText = "Demonstração simulada (Navegador sem suporte a Web Speech)";
    lizaReply.innerText = fallbackMsg;
    speakText(fallbackMsg);
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'pt-BR';
  recognition.interimResults = false;

  recognition.onstart = () => {
    micBtn.classList.add('listening');
    statusText.innerText = "Ouvindo... Pode falar agora!";
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.toLowerCase();
    userSpeech.innerText = '"' + transcript + '"';

    let reply = "Comando reconhecido! No aplicativo completo, executarei essa ação no seu computador.";

    if (transcript.includes("olá") || transcript.includes("oi") || transcript.includes("liza")) {
      reply = "Olá! Eu sou a Liza, uma assistente virtual de código aberto focada em acessibilidade.";
    } else if (transcript.includes("hora") || transcript.includes("horas")) {
      const agora = new Date();
      const h = agora.getHours();
      const m = agora.getMinutes();

      let textoHora = "";

      // Tratamento para Meia-noite, Meio-dia e horas normais
      if (h === 0) {
        textoHora = m === 0 ? "meia-noite em ponto" : `meia-noite e ${m} minuto${m > 1 ? 's' : ''}`;
      } else if (h === 12) {
        textoHora = m === 0 ? "meio-dia em ponto" : `meio-dia e ${m} minuto${m > 1 ? 's' : ''}`;
      } else {
        const prefixoHora = h === 1 ? "uma hora" : `${h} horas`;
        const sufixoMinuto = m === 0 ? "" : ` e ${m} minuto${m > 1 ? 's' : ''}`;
        textoHora = `${prefixoHora}${sufixoMinuto}`;
      }

      reply = (h === 1 && m === 0) ? "Agora é uma hora em ponto." : `Agora são ${textoHora}.`;
    } else if (transcript.includes("objetivo") || transcript.includes("quem é você")) {
      reply = "Meu objetivo é tornar o uso do computador mais acessível através de comandos de voz gratuitos.";
    }

    lizaReply.innerText = reply;
    speakText(reply);
  };

  recognition.onerror = () => {
    statusText.innerText = "Não foi possível ouvir. Verifique a permissão do microfone e tente novamente.";
  };

  recognition.onend = () => {
    micBtn.classList.remove('listening');
    statusText.innerText = "Clique no microfone para falar novamente";
  };

  recognition.start();
}