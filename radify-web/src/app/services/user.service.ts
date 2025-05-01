import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { CommonService } from './common.service'; // Adjust the import path as necessary
import { jwtDecode } from 'jwt-decode'; // Ensure you have jwt-decode installed

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private baseUrl = ''; // Replace with your actual backend URL

  constructor(
    private http: HttpClient, 
    private commonService: CommonService
  ) {
    this.baseUrl = this.commonService.getBaseUrl();
  }

  signup(user: { email: string; name: string; password: string }): Observable<any> {
    return this.http.post(`${this.baseUrl}/signup`, user);
  }

  signin(user: { email: string; password: string }) {
    return this.http.post<{ access_token: string }>(`${this.baseUrl}/signin`, user).pipe(
      tap((response) => {
        this.commonService.setValue('auth_token', response.access_token);
      })
    );
  }

  logout(): void {
    localStorage.removeItem('auth_token');
  }

  isLoggedIn(): boolean {
    return !!this.commonService.getValue('auth_token');
  }

  getUserEmail(): string | null {
    const token = this.commonService.getValue('auth_token');
    if (!token) return null;
    try {
      const decoded: any = jwtDecode(token);
      return decoded.sub || decoded.email;
    } catch {
      return null;
    }
  }
}