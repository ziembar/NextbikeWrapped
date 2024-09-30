import { Component, signal, ViewChild } from '@angular/core';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { InputNumber } from 'primeng/inputnumber';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
  providers: [MessageService]
})
export class LoginComponent {


  constructor(private apiService: ApiService, public router: Router, private formBuilder: FormBuilder,  private toast: MessageService) {}
  @ViewChild('inputnumber') inputnumber: InputNumber;

  error = signal(false)
  loading = signal(false)
  authorized = signal(false)
  duringReset = signal(false)


  error_message = 'Wprowadzono niepoprawne dane. Spróbuj ponownie.'

  cookie = localStorage.getItem('cookie');
  name = localStorage.getItem('name');
  exp = localStorage.getItem('exp');


  auth: FormGroup


  ngOnInit() {
    this.auth = this.formBuilder.group({
      phone: [, [Validators.required, Validators.pattern(/^[0-9]{9}$/), Validators.minLength(9), Validators.maxLength(9)]],
      pin: [, [Validators.required, Validators.minLength(5), Validators.maxLength(6)]]
    }, {updateOn: 'change'});

    setTimeout(
      ()=>{this.inputnumber.spin = () => {}}, 300)



    if(this.exp && this.cookie) {
      if(Date.now()/1000 < parseInt(this.exp)) {
          this.authorized.set(true)
      }
  }

  this.countries = [
    { name: 'Austria', code: 'AT', prefix: '+43' },
    { name: 'Switzerland', code: 'CH', prefix: '+41' },
    { name: 'Poland', code: 'PL', prefix: '+48' },
    { name: 'Turkey', code: 'TR', prefix: '+90' },
    { name: 'New Zealand', code: 'NZ', prefix: '+64' },
    { name: 'Latvia', code: 'LV', prefix: '+371' },
    { name: 'Cyprus', code: 'CY', prefix: '+357' },
    { name: 'Germany', code: 'DE', prefix: '+49' }
];
this.selectedCountry = { name: 'Poland', code: 'PL', prefix: '+48' }



}







countries: any[] | undefined;

selectedCountry: any;

toggleResetPage(){
this.duringReset.set(!this.duringReset());
}


submitAction(){
  if(this.duringReset()){
    this.resetPin();
  }else{
    this.login();
  }
}

resetPin(){
  console.log("RESET")
  this.loading.set(true)
  const phone = this.selectedCountry.prefix.replace('+', '') + this.auth.get('phone').value;
  this.apiService.resetPin(phone).subscribe((response: any)=> {
    if(response.code !== 200){
    this.toast.add({life:5000, severity: 'error', summary: 'Ups.. coś poszło nie tak', detail: "Spróbuj ponownie później..." });
    this.toggleResetPage();
    this.loading.set(false)

    return
    }
    else{
      this.toast.add({life:5000, severity: 'success', summary: 'Udało się!', detail: "Pin został wysłany na twój numer" });
      this.toggleResetPage();
      this.loading.set(false)

    }


  })
}


  login() {
    this.loading.set(true)
    const phone = this.selectedCountry.prefix.replace('+', '') + this.auth.get('phone').value;
    const pin = this.auth.get('pin').value
    this.apiService.login(phone, pin).subscribe((response: any) => {
      if(response.code !== 200) {
        this.error_message = response.statusText ?? 'Wprowadzono niepoprawne dane. Spróbuj ponownie.'
        this.error.set(true)
        this.loading.set(false)
        return;
      }
      this.loading.set(false)
      localStorage.setItem('cookie', response.cookie);
      const username = response.name.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

      localStorage.setItem('name', username);
      localStorage.setItem('exp', response.exp);
      this.router.navigate(['/summary']);
    }, error => {
      this.loading.set(false)
      this.error_message = error.statusText ?? 'Wystąpił nieznany błąd. Spróbuj ponownie później.'

      this.error.set(true)
        return;
    });
  }
}

