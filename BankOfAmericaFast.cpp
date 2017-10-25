//
//  main.cpp
//  amex
//
//  Created by JonLuca De Caro on 11/7/16.
//  Copyright © 2016 JonLuca De Caro. All rights reserved.
//  
//

#include <iostream>
#include <fstream>


// First attempt at generating URLs in c++ - very fast but a lot more verbose than the python version
int main(int argc, const char * argv[]) {
    // insert code here...
    using namespace std;
    std::ofstream myfile;
    myfile.open ("Documents/test/amex.txt");
    //https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=C&campaignid=4013729&productoffercode=T2
    for(int i = 0; i<99999; i++){
        if(i < 10){
            myfile << "https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=C&campaignid=400000" + to_string(i) + "&productoffercode=T2" + "\n";
        }else if(i < 100){
            myfile << "https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=C&campaignid=40000" + to_string(i) + "&productoffercode=T2" + "\n";

        }else if(i < 1000){
            myfile << "https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=C&campaignid=4000" + to_string(i) + "&productoffercode=T2" + "\n";

        }else if(i< 10000){
            myfile << "https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=C&campaignid=400" + to_string(i) + "&productoffercode=T2" + "\n";
        }else{
            myfile << "https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=C&campaignid=40" + to_string(i) + "&productoffercode=T2" + "\n";
        }
        //myfile << "https://secure.bankofamerica.com/applynow/initialize-workflow.go?requesttype=C&campaignid=401" + to_string(i) + "&productoffercode=T2" + "\n";
    }
    std::cout << "Done! \n";
    return 0;
}
