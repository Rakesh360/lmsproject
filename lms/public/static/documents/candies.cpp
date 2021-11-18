#include<bits/stdc++.h>
using namespace std;

int main()
{
	int t;
	cin>>t;
	while(t--)
	{
        long long n, k=2;cin>>n;
        long long temp = pow(2, k) - 1;
        while (n%temp != 0) {
            k+=1;
            temp = pow(2, k) - 1;
        }

        cout<<n/temp<<endl;
	}
	return 0;	
}