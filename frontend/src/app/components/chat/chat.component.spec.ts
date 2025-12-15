import { TestBed } from '@angular/core/testing';
import { ChatComponent } from './chat.component';

describe('Chat', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChatComponent],
    }).compileComponents();
  });

  it('should create the chat component', () => {
    const fixture = TestBed.createComponent(ChatComponent);
    const chat = fixture.componentInstance;
    expect(chat).toBeTruthy();
  });
});