import { Component, OnInit } from '@angular/core';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RadGenerationService } from '../services/rad-generation.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  imports: [FormsModule, CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {

  jobText: string = '';
  selectedFiles: File[] = [];
  isLoading: boolean = false;
  radContent: string = '';
  user = {
    id: 1,
    email: '',
    name: '',
    created_at: ''
  } // Replace with actual authenticated user ID if available
  errorMessage: string = '';

  constructor(
    private userService: UserService,
    private router: Router,
    private radService: RadGenerationService
  ) {}

  ngOnInit(): void {
    this.userService.verifyToken().subscribe({
      next: (res) => {
        this.user = {...res}
      }
    })
  }

  logout(): void {
    this.userService.logout();
    this.router.navigate(['/']);
  }

  onFileSelected(event: any) {
    this.selectedFiles = Array.from(event.target.files);
  }

  onSubmit(): void {
    if (!this.jobText && this.selectedFiles.length === 0) {
      this.errorMessage = 'Please enter job description or upload at least one file.';
      return;
    }

    const formData = new FormData();
    formData.append('job_text', this.jobText);
    formData.append('user_id', this.user.id.toString());

    this.selectedFiles.forEach(file => {
      formData.append('files', file);
    });

    this.isLoading = true;
    this.errorMessage = '';

    this.radService.generateRad(formData).subscribe({
      next: (res) => {
        this.radContent = res.rad_content;
        this.isLoading = false;
      },
      error: (err: HttpErrorResponse) => {
        this.errorMessage = err.error?.detail || 'An error occurred while generating the RAD.';
        this.isLoading = false;
      }
    });
  }
}
