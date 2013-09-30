
puts Process.getrlimit(Process::RLIMIT_CPU)
Process.setrlimit(Process::RLIMIT_CPU, 3598, 3600)
puts Process.getrlimit(Process::RLIMIT_CPU)

puts Process.getrlimit(Process::RLIMIT_CPU)
Process.setrlimit(Process::RLIMIT_CPU, 3598, 3600)
puts Process.getrlimit(Process::RLIMIT_CPU)
