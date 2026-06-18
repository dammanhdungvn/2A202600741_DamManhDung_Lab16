from __future__ import annotations
import json
from pathlib import Path
import typer
from rich import print
from dotenv import load_dotenv
load_dotenv()
from src.reflexion_lab.agents import ReActAgent, ReflexionAgent
from src.reflexion_lab.reporting import build_report, save_report
from src.reflexion_lab.utils import load_dataset, save_jsonl
app = typer.Typer(add_completion=False)

@app.command()
def main(dataset: str = "data/hotpot_mini.json", out_dir: str = "outputs/sample_run", reflexion_attempts: int = 3) -> None:
    examples = load_dataset(dataset)
    react = ReActAgent()
    reflexion = ReflexionAgent(max_attempts=reflexion_attempts)
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
    console.print(Panel(f"[bold magenta]🚀 Bắt đầu Benchmark[/bold magenta]\n[white]Dataset:[/white] {dataset}\n[white]Số lượng:[/white] {len(examples)} câu hỏi\n[white]Reflexion Max Attempts:[/white] {reflexion_attempts}", expand=False))

    react_records = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=False
    ) as progress:
        task1 = progress.add_task("[cyan]ReAct Agent...", total=len(examples))
        for example in examples:
            progress.update(task1, description=f"[cyan]ReAct đang xử lý:[/cyan] [bold]{example.qid}[/bold]")
            record = react.run(example)
            react_records.append(record)
            status = "[green]✅ ĐÚNG[/green]" if record.is_correct else "[red]❌ SAI[/red]"
            progress.console.print(f"   ↳ [cyan]ReAct[/cyan] | {example.qid}: {status} [dim](Tokens: {record.token_estimate}, {record.latency_ms}ms)[/dim]")
            progress.advance(task1)
            
    console.print()
            
    reflexion_records = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=False
    ) as progress:
        task2 = progress.add_task("[yellow]Reflexion Agent...", total=len(examples))
        for example in examples:
            progress.update(task2, description=f"[yellow]Reflexion đang xử lý:[/yellow] [bold]{example.qid}[/bold]")
            record = reflexion.run(example)
            reflexion_records.append(record)
            status = "[green]✅ ĐÚNG[/green]" if record.is_correct else "[red]❌ SAI[/red]"
            progress.console.print(f"   ↳ [yellow]Reflexion[/yellow] | {example.qid}: {status} [dim](Thử lại: {record.attempts} lần | Tokens: {record.token_estimate} | {record.latency_ms}ms)[/dim]")
            progress.advance(task2)
    
    console.print(Panel("[bold green]✅ Hoàn tất Benchmark![/bold green] Đang lưu kết quả...", expand=False))
    
    all_records = react_records + reflexion_records
    out_path = Path(out_dir)
    save_jsonl(out_path / "react_runs.jsonl", react_records)
    save_jsonl(out_path / "reflexion_runs.jsonl", reflexion_records)
    report = build_report(all_records, dataset_name=Path(dataset).name, mode="mock")
    json_path, md_path = save_report(report, out_path)
    print(f"[green]Saved[/green] {json_path}")
    print(f"[green]Saved[/green] {md_path}")
    from rich.table import Table
    summary = report.summary
    react_stats = summary.get("react", {})
    ref_stats = summary.get("reflexion", {})
    delta = summary.get("delta_reflexion_minus_react", {})
    
    table = Table(title="📊 Báo cáo Benchmark Tổng Quan", show_header=True, header_style="bold magenta", border_style="blue")
    table.add_column("Chỉ số", style="bold cyan", width=25)
    table.add_column("🤖 ReAct", justify="right", style="green")
    table.add_column("🧠 Reflexion", justify="right", style="yellow")
    table.add_column("📈 Khác biệt", justify="right", style="bold white")
    
    table.add_row(
        "Độ chính xác (EM)", 
        f"{react_stats.get('em', 0):.1%}", 
        f"{ref_stats.get('em', 0):.1%}", 
        f"+{delta.get('em_abs', 0):.1%}" if delta.get('em_abs', 0) > 0 else f"{delta.get('em_abs', 0):.1%}"
    )
    table.add_row(
        "Số lần sửa sai trung bình", 
        f"{react_stats.get('avg_attempts', 0):.1f}", 
        f"{ref_stats.get('avg_attempts', 0):.1f}", 
        f"+{delta.get('attempts_abs', 0):.1f}"
    )
    table.add_row(
        "Tokens tiêu thụ trung bình", 
        f"{react_stats.get('avg_token_estimate', 0):.0f}", 
        f"{ref_stats.get('avg_token_estimate', 0):.0f}", 
        f"+{delta.get('tokens_abs', 0):.0f}"
    )
    table.add_row(
        "Thời gian xử lý trung bình", 
        f"{react_stats.get('avg_latency_ms', 0):.0f}ms", 
        f"{ref_stats.get('avg_latency_ms', 0):.0f}ms", 
        f"+{delta.get('latency_abs', 0):.0f}ms"
    )
    
    console.print("\n")
    console.print(table)

if __name__ == "__main__":
    app()
