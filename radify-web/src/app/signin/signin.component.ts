import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonService } from '../services/common.service';
import { Router } from '@angular/router';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-signin',
  imports: [FormsModule, CommonModule],
  templateUrl: './signin.component.html',
  styleUrl: './signin.component.css'
})
export class SigninComponent {
  isSignUpMode: boolean = false;
  user = {
    email: '',
    name: '',
    password: '',
    confirmPassword: ''
  };

  showPassword: boolean = false;
  showConfirmPassword: boolean = false;

  constructor(
    private commonService: CommonService,
    private router: Router,
    private userService: UserService
  ) {}

  toggleMode(event: Event): void {
    event.preventDefault();
    this.isSignUpMode = !this.isSignUpMode;
    this.clearForm();
  }

  signInWithGoogle(): void {
    window.location.href = this.commonService.getBaseUrl() + '/auth/google';
  }

  onSubmit(): void {
    if (this.isSignUpMode) {
      if (this.user.password !== this.user.confirmPassword) {
        alert("Passwords do not match.");
        return;
      }
  
      this.userService.signup(this.user).subscribe({
        next: (response) => {
          alert("Signup successful! Please sign in.");
          this.toggleMode(new Event('submit'));
        },
        error: (err) => alert("Signup failed: " + err.message)
      });
    } else {
      this.userService.signin({
        email: this.user.email,
        password: this.user.password
      }).subscribe({
        next: (response) => {
          // Token already stored via tap
          this.router.navigate(['/dashboard']);  // or any protected route
        },
        error: (err) => alert("Signin failed: " + err.message)
      });
    }
  }

  clearForm(): void {
    this.user.email = '';
    this.user.name = '';
    this.user.password = '';
    this.user.confirmPassword = '';
  }
}
