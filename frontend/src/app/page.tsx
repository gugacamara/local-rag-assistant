import Chat from "../components/Chat";
import FileUpload from "../components/FileUpload";

export default function Home() {
  return (
    <main className="min-h-screen bg-white flex flex-col items-center py-10 gap-8">
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold text-gray-900 tracking-tight">
          Local RAG Assistant
        </h1>
        <p className="text-gray-500">
          Converse com seus PDFs de forma privada
        </p>
      </div>

      <FileUpload />
      <Chat />
    </main>
  );
}