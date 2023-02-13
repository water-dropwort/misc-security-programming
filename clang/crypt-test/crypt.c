#include<unistd.h>
#include<stdio.h>

int main(void)
{
  printf("%s:%s\n", "user0", crypt("cat", "$1$h6fC1Os1$"));
  return 0;
}
