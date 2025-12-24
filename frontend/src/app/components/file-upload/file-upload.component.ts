import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatService } from '../../services/chat.service';

@Component({
  selector: 'app-file-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './file-upload.component.html',
  styleUrl: './file-upload.component.css'
})
export class FileUploadComponent {
  isUploading = signal(false);
  uploadStatus = signal<string>('');

  constructor(private chatService: ChatService) {}

  async onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const file = input.files[0];
    this.isUploading.set(true);
    this.uploadStatus.set(`Enviando ${file.name}...`);

    try {
      const result = await this.chatService.uploadFile(file);
      this.uploadStatus.set(`✅ Sucesso! ${result.chunks} trechos indexados.`);
    } catch (error) {
      this.uploadStatus.set('❌ Erro ao enviar arquivo: ' + (error as Error).message);
      console.error(error);
    } finally {
      this.isUploading.set(false);
      input.value = ''; // Limpar input
    }
  }
}
