#define ena 11 
#define enb 3
#define in1 10
#define in2 9
#define in3 6
#define in4 5

#define fast 255   //pwm for soft turn
#define slow 100  //pwm for hard turn

void forward()                                                           //forward
{
   digitalWrite(in1,HIGH);
   digitalWrite(in2,LOW);

   digitalWrite(in3,LOW);
   digitalWrite(in4,HIGH);
    
   analogWrite(ena,fast);
   analogWrite(enb,fast); 
}

void backward()                                                           //backward
{
   digitalWrite(in1,LOW);
   digitalWrite(in2,HIGH);

   digitalWrite(in3,HIGH);
   digitalWrite(in4,LOW);
    
   analogWrite(ena,fast);
   analogWrite(enb,slow); 
}

void pause()                                                           //pause
{
   digitalWrite(in1,HIGH);
   digitalWrite(in2,HIGH);

   digitalWrite(in3,LOW);
   digitalWrite(in4,LOW);
    
   //analogWrite(ena,spwm);
   //analogWrite(enb,spwm); 
}

void setup() {
  // put your setup code here, to run once:
  pinMode(ena,OUTPUT);
  pinMode(in1,OUTPUT);
  pinMode(in2,OUTPUT);
  pinMode(enb,OUTPUT);
  pinMode(in3,OUTPUT);
  pinMode(in4,OUTPUT);

  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
   String c;
   c = Serial.readString(); 
   //forward();
   if(c.equals("fw")){
      forward();
   }
   if(c=="bw"){
     backward();
   }
   if(c=="pw"){
     pause();
   }
   
}
