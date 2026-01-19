"use client";
import { useState } from 'react';
import { uploadFile } from '../services/api';

export default function FileUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileSelected = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    setStatus(`Enviando ${file.name}...`);

    try {
      const result = await uploadFile(file);
      setStatus(`✅ Sucesso! ${result.chunks} trechos indexados.`);
    } catch (error) {
      console.error(error);
      setStatus('❌ Erro ao enviar arquivo.');
    } finally {
      setIsUploading(false);
      event.target.value = '';
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-4 flex flex-col items-center gap-4">
      <label className={`
        flex items-center gap-2 px-6 py-3 rounded-full cursor-pointer transition-all shadow-sm border
        ${isUploading 
          ? 'bg-gray-100 text-gray-500 border-gray-300 cursor-not-allowed' 
          : 'bg-white hover:bg-gray-50 text-blue-600 border-blue-200 hover:border-blue-400'}
      `}>
        <input 
          type="file" 
          accept=".pdf" 
          onChange={handleFileSelected} 
          disabled={isUploading} 
          className="hidden" 
        />
        <span className="font-medium">
          {isUploading ? '⏳ Processando PDF...' : '📎 Adicionar PDF ao RAG'}
        </span>
      </label>

      {status && (
        <div className="text-sm font-medium text-gray-600 animate-pulse">
          {status}
        </div>
      )}
    </div>
  );
}