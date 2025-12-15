import { TestBed } from '@angular/core/testing';
import { FileUploadComponent } from './file-upload.component';

describe('FileUploadComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FileUploadComponent],
    }).compileComponents();
  });

  it('should create the file upload component', () => {
    const fixture = TestBed.createComponent(FileUploadComponent);
    const fileUpload = fixture.componentInstance;
    expect(fileUpload).toBeTruthy();
  });
});