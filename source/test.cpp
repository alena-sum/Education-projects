#include <fstream>
#include <iostream>

using namespace std;

int main() {
    fstream cin("connection.json");
    std::string str;
    cin >> str;
    cout << str;
}
