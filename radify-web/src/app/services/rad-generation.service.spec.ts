import { TestBed } from '@angular/core/testing';

import { RadGenerationService } from './rad-generation.service';

describe('RadGenerationService', () => {
  let service: RadGenerationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RadGenerationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
