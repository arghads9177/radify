import { Component } from '@angular/core';
import { UserService } from '../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {

  constructor(
    private userService: UserService,
    private router: Router
  ) {}

  logout(): void {
    this.userService.logout();
    this.router.navigate(['/']);
  }
}
