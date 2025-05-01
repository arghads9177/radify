import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CommonService {

  constructor() { }

  private base_url = 'http://localhost:8000';

  getBaseUrl() {
    return this.base_url;
  }

  setValue(key: string, token: string): void {
    localStorage.setItem(key, token);
  }
  
  getValue(key: string): string | null {
    return localStorage.getItem(key);
  }
}
