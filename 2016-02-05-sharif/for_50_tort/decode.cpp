#include <iostream>
#include <iomanip> 
using namespace std;  
int data[][23];
int indexOf(int num){ 
	for(int x=0; x<256; x++){ 	
		if(num == lookup[x]){ 		
			return x; 	
		}
	} 	
	return -1;
}  
int main(){ 	  	
	for(int i=0; i<14747; i++){ 		
		for(int j=0; j<23; j++){ 		
			cout << hex << setfill('0') << setw(2) << indexOf(data[i][j]); 	
		} 
	} 
}