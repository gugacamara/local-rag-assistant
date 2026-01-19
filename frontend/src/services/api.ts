const API_URL = 'http://localhost:8000';

export const uploadFile = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Erro ao enviar arquivo');
  }
  return data;
};

export const sendMessage = async (query: string, onChunk: (text: string) => void) => {
  const response = await fetch(`${API_URL}/chat?query=${encodeURIComponent(query)}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.body) return;

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    // Decodifica o pedaço e manda para quem chamou a função
    onChunk(decoder.decode(value, { stream: true }));
  }
};