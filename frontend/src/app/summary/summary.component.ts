import { Component, OnInit, signal } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';


@Component({
  selector: 'app-summary',
  templateUrl: 'summary.component.html',
  styleUrls: ['summary.component.css'],
  providers: [MessageService]
})
export class SummaryComponent {
  
    constructor(private apiService: ApiService, private router: Router, private toast: MessageService) {}
    data = signal(undefined);
    season = signal({name: undefined, startValue: undefined, endValue: undefined});
    loading = signal(false);
    name = localStorage.getItem('name');

    ngOnInit() {
      const cookie = localStorage.getItem('cookie');
      const exp = localStorage.getItem('exp');
      
      const urlParams = new URLSearchParams(window.location.search);
      const id = urlParams.get('id');

      if(!id){
        if(exp && cookie) {
          if(Date.now()/1000 > parseInt(exp)) {
              this.router.navigate(['/login']);
              return
          }
        }
        else {
          this.router.navigate(['/login']);
          return
        }
        this.setSeason({name: new Date().getFullYear().toString(), startValue: null, endValue: null});
        return
      }
      this.getData(null, id);
    }

  setSeason(season: {name: string, startValue: any, endValue: any}) {
    this.season.set(season);
    this.data.set(undefined)

    this.getData(season, null);
  }


  back() {
    this.data.set(undefined);
    this.loading.set(false);
  }

  


  getData(season: any, id: any){
    this.loading.set(true);
    if(id){
      this.apiService.getData(null, null, null, id).subscribe((response: any) => {
        this.data.set(response);
        const url = new URL(window.location.href);
        url.searchParams.set('id', response.id);
        window.history.replaceState({}, '', url.toString());
        this.loading.set(false);
      }, error => {
        this.toast.add({life:5000, severity: 'error', summary: 'Ups.. coś poszło nie tak', detail: error.statusText });
        this.loading.set(false);
      });
      return
    }

    let cookie = '';
    try{
        cookie = localStorage.getItem('cookie');
        if (cookie === null) {
          this.loading.set(false);
          this.toast.add({ severity: 'error', summary: 'Hmm.. spróbuj ponownie się zalogować', detail: 'Token not found' });
          throw 'Token not found';
        }
    }catch(e){
        this.loading.set(false);
        this.router.navigate(['/login']);
        return;
    }

    this.apiService.getData(season, cookie, this.name, null).subscribe((response: any) => {
      this.data.set(response);
      const url = new URL(window.location.href);
      url.searchParams.set('id', response.id);
      window.history.replaceState({}, '', url.toString());
      this.loading.set(false);
    }, error => {
      this.toast.add({life:5000, severity: 'error', summary: 'Ups.. coś poszło nie tak', detail: error.statusText });
      this.loading.set(false);
    });
  }
}