import { Component, signal } from '@angular/core'; // <--- Importante: signal
import { FormsModule } from '@angular/forms';
import { ChatService } from './services/chat.service';
import { FileUploadComponent } from './components/file-upload/file-upload.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FormsModule, FileUploadComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  userQuery = ''; 
  
  responseBuffer = signal<string>(''); 
  isLoading = signal<boolean>(false);

  constructor(private chatService: ChatService) {}

  async send() {
    if (!this.userQuery.trim()) return;

    this.responseBuffer.set('');
    this.isLoading.set(true);
    
    const queryToSend = this.userQuery;

    try {
      await this.chatService.sendMessage(queryToSend, (chunk) => {
        this.responseBuffer.update(old => old + chunk);
      });
    } catch (error) {
      console.error('Erro no chat:', error);
      this.responseBuffer.set('Erro ao conectar com o servidor.');
    } finally {
      this.isLoading.set(false);
    }
  }
}