import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
@Injectable({
  providedIn: 'root'
})
@Injectable()
export class ApiService {
  httpClient:HttpClient;
  constructor() { }
  getDataSet():any{
    return this.
    httpClient.
    get<any[]>("https://data.culture.gouv.fr/api/records/1.0/search/?dataset=frequentation-dans-les-salles-de-cinema&q=&rows=100&sort=annee&facet=annee")
  }
}
