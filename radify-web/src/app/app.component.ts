import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from './services/user.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  constructor(private router: Router, private userService: UserService) {}

  title = 'radify-web';

  ngOnInit(): void {
    if (this.userService.isLoggedIn()) {
      this.router.navigate(['/dashboard']);
    }
  }
}