// src/app/services/rad-generation.service.ts

import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CommonService } from './common.service';

@Injectable({
  providedIn: 'root'
})
export class RadGenerationService {
  private baseUrl = '';

  constructor(
    private http: HttpClient,
    private commonService: CommonService
  ) {
    this.baseUrl = this.commonService.getBaseUrl(); // Ensure this returns something like http://localhost:8000
  }

  generateRad(formData: FormData): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/rad/generate`, formData);
  }
}
