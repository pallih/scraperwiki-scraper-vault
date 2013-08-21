#Process.setrlimit(Process::RLIMIT_CPU, 2, 3)

def moo()
  x = 100000
  for i in 1..10000000 do
      x = x * i
      if i % 1000 == 0 then
          used = Process.getrusage()
          puts i.to_s + " " + x.to_s.size.to_s rescue "CPU?"
          puts Process.getrlimit(Process::RLIMIT_CPU), used[0], used[1]
      end
  end
end

moo()


