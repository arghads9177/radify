import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../services/user.service';
import { CommonService } from '../services/common.service';

@Component({
  selector: 'app-auth-callback',
  template: ''
})
export class AuthCallbackComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private commonService: CommonService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      const token = params['access-token'];
      if (token) {
        this.commonService.setValue('auth_token', token);
        this.router.navigate(['/dashboard']);  // Redirect to dashboard
      } else {
        this.router.navigate(['/signin']);
      }
    });
  }
}
