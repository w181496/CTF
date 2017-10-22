#include <iostream>
#include <string>
#include <fstream>
using namespace std;
int main() {
    string s;
    ifstream fin("flag-ee94f5c9452a6db022db1e4f3a036b375b3ac472");
    getline(fin, s);
    for(int i = 0; i < 38  ; ++i) {
        int sum = 0;
        int a = (unsigned char)s[4*i+2];
        int b = (unsigned char)s[4*i+1];
        int c = (unsigned char)s[4*i];
        sum += a * 256 * 256 + b * 256 + c;
        sum -= 9011;
        char ch = sum / ((i + 1) << ((i + 2) % 0xa));
        cout << ch;
    }
    cout << endl;
    return 0;
}
