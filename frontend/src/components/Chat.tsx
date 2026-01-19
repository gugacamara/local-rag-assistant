"use client";
import { useState } from 'react';
import { sendMessage } from '../services/api';

export default function Chat() {
  const [userQuery, setUserQuery] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!userQuery.trim()) return;

    setIsLoading(true);
    setResponse('');

    try {
      await sendMessage(userQuery, (chunk) => {
        setResponse((prev) => prev + chunk);
      });
    } catch (error) {
      console.error(error);
      setResponse('Erro ao conectar com o servidor.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4">
      {/* Área de Input */}
      <div className="flex gap-2 mb-6">
        <input
          type="text"
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-black"
          placeholder="Pergunte algo sobre seus documentos..."
          value={userQuery}
          onChange={(e) => setUserQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !userQuery.trim()}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors font-medium"
        >
          {isLoading ? 'Gerando...' : 'Enviar'}
        </button>
      </div>

      {/* Área de Resposta */}
      {response && (
        <div className="bg-gray-50 border border-gray-200 rounded-xl p-6 shadow-sm">
          <h3 className="text-gray-700 font-bold mb-2">Resposta:</h3>
          <p className="whitespace-pre-wrap text-gray-800 leading-relaxed">
            {response}
          </p>
        </div>
      )}
    </div>
  );
}