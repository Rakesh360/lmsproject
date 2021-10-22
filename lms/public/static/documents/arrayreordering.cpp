#include<bits/stdc++.h>
using namespace std;

int main()
{
	int t;
	cin>>t;
	while(t--)
	{
        int n; cin>>n;
        // vector<int> a(n);
        int a[n];
        for (int i = 0; i < n; i++)
        {
            cin>>a[i];
        }
        sort(a, a + n);
        int ans = 0;
        for (int i = 0; i < n; ++i)
        {
            for (int j = i+1; j < n; ++j)
            {
                // cout<<a[i]<<a[j]<<endl;
                ans += __gcd(a[i], 2*a[j]) > 1;
            }
            
        }

        cout<<ans<<endl;

	}
	return 0;	
}